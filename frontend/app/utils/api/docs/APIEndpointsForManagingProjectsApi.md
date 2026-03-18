# APIEndpointsForManagingProjectsApi

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**createProjectProjectsPost**](APIEndpointsForManagingProjectsApi.md#createprojectprojectspost) | **POST** /projects/ | Create Project |
| [**deleteProjectProjectsProjectIdDelete**](APIEndpointsForManagingProjectsApi.md#deleteprojectprojectsprojectiddelete) | **DELETE** /projects/{project_id} | Delete Project |
| [**getProjectProjectsProjectIdGet**](APIEndpointsForManagingProjectsApi.md#getprojectprojectsprojectidget) | **GET** /projects/{project_id} | Get Project |
| [**listProjectsProjectsGet**](APIEndpointsForManagingProjectsApi.md#listprojectsprojectsget) | **GET** /projects/ | List Projects |
| [**updateProjectProjectsProjectIdPatch**](APIEndpointsForManagingProjectsApi.md#updateprojectprojectsprojectidpatch) | **PATCH** /projects/{project_id} | Update Project |



## createProjectProjectsPost

> CreateProjectResponse createProjectProjectsPost(createProjectRequest)

Create Project

### Example

```ts
import {
  Configuration,
  APIEndpointsForManagingProjectsApi,
} from '';
import type { CreateProjectProjectsPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForManagingProjectsApi();

  const body = {
    // CreateProjectRequest
    createProjectRequest: ...,
  } satisfies CreateProjectProjectsPostRequest;

  try {
    const data = await api.createProjectProjectsPost(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **createProjectRequest** | [CreateProjectRequest](CreateProjectRequest.md) |  | |

### Return type

[**CreateProjectResponse**](CreateProjectResponse.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **201** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## deleteProjectProjectsProjectIdDelete

> MessageResponse deleteProjectProjectsProjectIdDelete(projectId)

Delete Project

### Example

```ts
import {
  Configuration,
  APIEndpointsForManagingProjectsApi,
} from '';
import type { DeleteProjectProjectsProjectIdDeleteRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForManagingProjectsApi();

  const body = {
    // number
    projectId: 56,
  } satisfies DeleteProjectProjectsProjectIdDeleteRequest;

  try {
    const data = await api.deleteProjectProjectsProjectIdDelete(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **projectId** | `number` |  | [Defaults to `undefined`] |

### Return type

[**MessageResponse**](MessageResponse.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## getProjectProjectsProjectIdGet

> ProjectResponse getProjectProjectsProjectIdGet(projectId)

Get Project

### Example

```ts
import {
  Configuration,
  APIEndpointsForManagingProjectsApi,
} from '';
import type { GetProjectProjectsProjectIdGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForManagingProjectsApi();

  const body = {
    // number
    projectId: 56,
  } satisfies GetProjectProjectsProjectIdGetRequest;

  try {
    const data = await api.getProjectProjectsProjectIdGet(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **projectId** | `number` |  | [Defaults to `undefined`] |

### Return type

[**ProjectResponse**](ProjectResponse.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## listProjectsProjectsGet

> Array&lt;ProjectResponse&gt; listProjectsProjectsGet()

List Projects

### Example

```ts
import {
  Configuration,
  APIEndpointsForManagingProjectsApi,
} from '';
import type { ListProjectsProjectsGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForManagingProjectsApi();

  try {
    const data = await api.listProjectsProjectsGet();
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

This endpoint does not need any parameter.

### Return type

[**Array&lt;ProjectResponse&gt;**](ProjectResponse.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)


## updateProjectProjectsProjectIdPatch

> ProjectResponse updateProjectProjectsProjectIdPatch(projectId, updateProjectRequest)

Update Project

### Example

```ts
import {
  Configuration,
  APIEndpointsForManagingProjectsApi,
} from '';
import type { UpdateProjectProjectsProjectIdPatchRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForManagingProjectsApi();

  const body = {
    // number
    projectId: 56,
    // UpdateProjectRequest
    updateProjectRequest: ...,
  } satisfies UpdateProjectProjectsProjectIdPatchRequest;

  try {
    const data = await api.updateProjectProjectsProjectIdPatch(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters


| Name | Type | Description  | Notes |
|------------- | ------------- | ------------- | -------------|
| **projectId** | `number` |  | [Defaults to `undefined`] |
| **updateProjectRequest** | [UpdateProjectRequest](UpdateProjectRequest.md) |  | |

### Return type

[**ProjectResponse**](ProjectResponse.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

