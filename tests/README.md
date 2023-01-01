# Tests

This package contains a test suite to test what little I can programmatically.
Many of the endpoints require OAuth verification, which there is no consistent
way to automate with something like a [GitHub action](/.github/workflows/test_api_endpoints_workflow.yml).

## Test Comprehension

#### OAuth Endpoints

| Endpoint        | Local              | Automated | Comments                                |
|-----------------|--------------------|-----------|-----------------------------------------|
| GetAccessToken  | :heavy_check_mark: | :x:       | Cannot automate test due to OAuth flow. |
| GetRefreshToken | :heavy_check_mark: | :x:       | Cannot automate test due to OAuth flow. |
    