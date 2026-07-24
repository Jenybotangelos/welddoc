from flask import Blueprint, redirect, request, session, jsonify, current_app
import uuid

try:
    import msal
except ImportError:
    msal = None

auth_bp = Blueprint("auth", __name__)

AUTHORITY_TEMPLATE = "https://login.microsoftonline.com/{tenant}"
SCOPES = ["User.Read"]


def _build_msal_app():
    return msal.ConfidentialClientApplication(
        current_app.config["AZURE_CLIENT_ID"],
        authority=AUTHORITY_TEMPLATE.format(tenant=current_app.config["AZURE_TENANT_ID"]),
        client_credential=current_app.config["AZURE_CLIENT_SECRET"],
    )


def _get_redirect_uri():
    # Azure requires http://localhost (not 127.0.0.1) or https://
    scheme = request.headers.get("X-Forwarded-Proto", request.scheme)
    host = request.host
    # Replace 127.0.0.1 with localhost for Azure App Registration compatibility
    if "127.0.0.1" in host:
        host = host.replace("127.0.0.1", "localhost")
    return f"{scheme}://{host}/auth/callback"


@auth_bp.route("/login")
def login():
    if msal is None:
        return "msal not installed on server. Run: pip install msal", 500
    session["state"] = str(uuid.uuid4())
    cca = _build_msal_app()
    auth_url = cca.get_authorization_request_url(
        SCOPES,
        state=session["state"],
        redirect_uri=_get_redirect_uri(),
        response_type="code",
    )
    return redirect(auth_url)


@auth_bp.route("/auth/callback", methods=["GET", "POST"])
def auth_callback():
    # Microsoft may POST (form_post) or GET depending on response_mode
    params = request.form if request.method == "POST" else request.args

    if params.get("state") != session.get("state"):
        return "State mismatch — possible CSRF. <a href='/'>Try again</a>", 403

    if "error" in params:
        return f"Login error: {params['error_description']}", 400

    code = params.get("code")
    if not code:
        return "No authorization code received.", 400

    cca = _build_msal_app()
    result = cca.acquire_token_by_authorization_code(
        code,
        scopes=SCOPES,
        redirect_uri=_get_redirect_uri(),
    )

    if "error" in result:
        return f"Token error: {result.get('error_description')}", 400

    # Extract user info from ID token claims
    claims = result.get("id_token_claims", {})
    email = claims.get("preferred_username", "").lower()
    name = claims.get("name", "")

    # Restrict to @botangelos.com only
    if not email.endswith("@botangelos.com"):
        session.clear()
        return (
            "<h2>Access Denied</h2>"
            "<p>Only @botangelos.com accounts are allowed.</p>"
            "<a href='/'>Back</a>"
        ), 403

    # Store user in session
    session["user"] = {
        "email": email,
        "name": name,
        "role": "office",
    }

    return redirect("/home.html")


@auth_bp.route("/auth/me")
def auth_me():
    user = session.get("user")
    if not user:
        return jsonify({"logged_in": False}), 401
    return jsonify({"logged_in": True, **user})


@auth_bp.route("/logout")
def logout():
    session.clear()
    # Redirect to Microsoft logout then back to our app
    tenant = current_app.config["AZURE_TENANT_ID"]
    scheme = request.headers.get("X-Forwarded-Proto", request.scheme)
    post_logout = f"{scheme}://{request.host}/"
    return redirect(
        f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/logout"
        f"?post_logout_redirect_uri={post_logout}"
    )
