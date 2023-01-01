# Bungie API Python Wrapper

This is a work in progress python wrapper for the Bungie API.

[MIT License](LICENSE.md)

[Test Status](tests/README.md)


### Planned Features

- [ ] Complete API coverage.
  - [x] OAuth workflow
    - [x] Token endpoints (access token, refresh token)
    - [x] OAuth context for endpoints requiring it.
  - [ ] Endpoints
    - [ ] App
    - [ ] User
    - [ ] Content
    - [ ] Forum
    - [ ] GroupV2
    - [ ] Tokens
    - [ ] Destiny2
    - [ ] CommunityContent
    - [ ] Trending
    - [ ] Fireteam
    - [ ] Social
    - [ ] Common
  - [ ] Entity Models
- [x] Async and sync client implementations.

---

## Notes

- I plan to create a separate package specifically for integrating with the
Destiny manifest, which will utilize this package as a dependency.