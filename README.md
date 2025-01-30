# Todo App with session based authentication.
Currently very basic level of session based authentication has been implemented:
When user logges in its session ID will be attached to request object which is sent to client.
# Future functionality about session based authentication:
## Session Security

- **Secure session cookies** using:
  - `HttpOnly`
  - `Secure`
  - `SameSite` attributes

- **Protection against:**
  - Session hijacking
  - Cross-Site Request Forgery (CSRF) attacks

---

## Session Management

- **How to log out a user** (e.g., delete the session)
- **Clearing expired sessions**

### Session Data Storage Options

- **Database-based**
- **Cache-based**
  - Redis
  - Memcached
- **File-based**
