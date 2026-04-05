# ProjectsApi

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**createProjectProjectsPost**](ProjectsApi.md#createprojectprojectspost) | **POST** /projects/ | Create Project |
| [**deleteProjectProjectsProjectIdDelete**](ProjectsApi.md#deleteprojectprojectsprojectiddelete) | **DELETE** /projects/{project_id} | Delete Project |
| [**getProjectProjectsProjectIdGet**](ProjectsApi.md#getprojectprojectsprojectidget) | **GET** /projects/{project_id} | Get Project |
| [**listProjectsProjectsGet**](ProjectsApi.md#listprojectsprojectsget) | **GET** /projects/ | List Projects |
| [**updateProjectProjectsProjectIdPatch**](ProjectsApi.md#updateprojectprojectsprojectidpatch) | **PATCH** /projects/{project_id} | Update Project |



## createProjectProjectsPost

> CreateProjectResponse createProjectProjectsPost(createProjectRequest)

Create Project

Create a new project.  Args:         body (CreateProjectRequest): name (str), description (str | None).  Returns:         CreateProjectResponse: Confirmation message and the new project_id (int).

### Example

```ts
import {
  Configuration,
  ProjectsApi,
} from '';
import type { CreateProjectProjectsPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new ProjectsApi();

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

Delete a project by its id. Does not automatically delete associated Bronze, Silver, or Gold resources.  Args:         project_id (int): The id of the project to delete.  Returns:         MessageResponse: Confirmation message.

### Example

```ts
import {
  Configuration,
  ProjectsApi,
} from '';
import type { DeleteProjectProjectsProjectIdDeleteRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new ProjectsApi();

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

Return a single project by its id.  Args:         project_id (int): The id of the project.  Returns:         ProjectResponse: Project id, name, description, and created_at. 404 if                 not found.

### Example

```ts
import {
  Configuration,
  ProjectsApi,
} from '';
import type { GetProjectProjectsProjectIdGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new ProjectsApi();

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

Return all projects. Use project_id from the results to scope Bronze, Silver, and Gold resource operations.  Returns:         list[ProjectResponse]: All projects with id, name, description, and created_at.

### Example

```ts
import {
  Configuration,
  ProjectsApi,
} from '';
import type { ListProjectsProjectsGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new ProjectsApi();

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

Update the name and/or description of a project.  Args:         project_id (int): The id of the project to update.         body (UpdateProjectRequest): name (str | None), description (str | None).                 Both fields are optional.  Returns:         ProjectResponse: Updated project data. 404 if not found.

### Example

```ts
import {
  Configuration,
  ProjectsApi,
} from '';
import type { UpdateProjectProjectsProjectIdPatchRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new ProjectsApi();

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

