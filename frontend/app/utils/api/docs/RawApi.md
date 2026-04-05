# RawApi

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**activateVersionRawResourceIdVersionsVersionPatch**](RawApi.md#activateversionrawresourceidversionsversionpatch) | **PATCH** /raw/{resource_id}/versions/{version} | Activate Version |
| [**createResourceRawPost**](RawApi.md#createresourcerawpost) | **POST** /raw/ | Create Resource |
| [**deleteResourceRawResourceIdDelete**](RawApi.md#deleteresourcerawresourceiddelete) | **DELETE** /raw/{resource_id} | Delete Resource |
| [**deleteVersionRawResourceIdVersionsVersionDelete**](RawApi.md#deleteversionrawresourceidversionsversiondelete) | **DELETE** /raw/{resource_id}/versions/{version} | Delete Version |
| [**downloadVersionRawResourceIdVersionsVersionGet**](RawApi.md#downloadversionrawresourceidversionsversionget) | **GET** /raw/{resource_id}/versions/{version} | Download Version |
| [**getResourceRawResourceIdGet**](RawApi.md#getresourcerawresourceidget) | **GET** /raw/{resource_id} | Get Resource |
| [**listResourcesRawGet**](RawApi.md#listresourcesrawget) | **GET** /raw/ | List Resources |
| [**listVersionsRawResourceIdVersionsGet**](RawApi.md#listversionsrawresourceidversionsget) | **GET** /raw/{resource_id}/versions | List Versions |
| [**updateResourceRawResourceIdPatch**](RawApi.md#updateresourcerawresourceidpatch) | **PATCH** /raw/{resource_id} | Update Resource |
| [**uploadVersionRawResourceIdVersionsPost**](RawApi.md#uploadversionrawresourceidversionspost) | **POST** /raw/{resource_id}/versions | Upload Version |



## activateVersionRawResourceIdVersionsVersionPatch

> MessageResponse activateVersionRawResourceIdVersionsVersionPatch(resourceId, version)

Activate Version

Set a specific version of a Raw layer resource as the active version.  Args:         resource_id (int): The id of the Raw resource.         version (int): The version number to activate.  Returns:         MessageResponse: Confirmation message. 404 if the version does not exist.

### Example

```ts
import {
  Configuration,
  RawApi,
} from '';
import type { ActivateVersionRawResourceIdVersionsVersionPatchRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new RawApi();

  const body = {
    // number
    resourceId: 56,
    // number
    version: 56,
  } satisfies ActivateVersionRawResourceIdVersionsVersionPatchRequest;

  try {
    const data = await api.activateVersionRawResourceIdVersionsVersionPatch(body);
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
| **resourceId** | `number` |  | [Defaults to `undefined`] |
| **version** | `number` |  | [Defaults to `undefined`] |

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


## createResourceRawPost

> CreateResourceResponse createResourceRawPost(createResourceRequest)

Create Resource

Create a new Raw layer resource.  Args:         body (CreateResourceRequest): name (str), project_id (int),                 description (str | None).  Returns:         CreateResourceResponse: Confirmation message and the new resource_id (int).

### Example

```ts
import {
  Configuration,
  RawApi,
} from '';
import type { CreateResourceRawPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new RawApi();

  const body = {
    // CreateResourceRequest
    createResourceRequest: ...,
  } satisfies CreateResourceRawPostRequest;

  try {
    const data = await api.createResourceRawPost(body);
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
| **createResourceRequest** | [CreateResourceRequest](CreateResourceRequest.md) |  | |

### Return type

[**CreateResourceResponse**](CreateResourceResponse.md)

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


## deleteResourceRawResourceIdDelete

> MessageResponse deleteResourceRawResourceIdDelete(resourceId)

Delete Resource

Delete a Raw layer resource and all its associated versions.  Args:         resource_id (int): The id of the Raw resource to delete.  Returns:         MessageResponse: Confirmation message.

### Example

```ts
import {
  Configuration,
  RawApi,
} from '';
import type { DeleteResourceRawResourceIdDeleteRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new RawApi();

  const body = {
    // number
    resourceId: 56,
  } satisfies DeleteResourceRawResourceIdDeleteRequest;

  try {
    const data = await api.deleteResourceRawResourceIdDelete(body);
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
| **resourceId** | `number` |  | [Defaults to `undefined`] |

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


## deleteVersionRawResourceIdVersionsVersionDelete

> MessageResponse deleteVersionRawResourceIdVersionsVersionDelete(resourceId, version)

Delete Version

Delete a specific version of a Raw layer resource, removing it from S3 and the database.  Args:         resource_id (int): The id of the Raw resource.         version (int): The version number to delete.  Returns:         MessageResponse: Confirmation message. 404 if the version does not exist.

### Example

```ts
import {
  Configuration,
  RawApi,
} from '';
import type { DeleteVersionRawResourceIdVersionsVersionDeleteRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new RawApi();

  const body = {
    // number
    resourceId: 56,
    // number
    version: 56,
  } satisfies DeleteVersionRawResourceIdVersionsVersionDeleteRequest;

  try {
    const data = await api.deleteVersionRawResourceIdVersionsVersionDelete(body);
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
| **resourceId** | `number` |  | [Defaults to `undefined`] |
| **version** | `number` |  | [Defaults to `undefined`] |

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


## downloadVersionRawResourceIdVersionsVersionGet

> any downloadVersionRawResourceIdVersionsVersionGet(resourceId, version)

Download Version

Download the raw file for a specific version of a Raw layer resource.  Args:         resource_id (int): The id of the Raw resource.         version (int): The version number to download.  Returns:         StreamingResponse: The raw file as an octet-stream attachment. 404 if the file                 is not found.

### Example

```ts
import {
  Configuration,
  RawApi,
} from '';
import type { DownloadVersionRawResourceIdVersionsVersionGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new RawApi();

  const body = {
    // number
    resourceId: 56,
    // number
    version: 56,
  } satisfies DownloadVersionRawResourceIdVersionsVersionGetRequest;

  try {
    const data = await api.downloadVersionRawResourceIdVersionsVersionGet(body);
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
| **resourceId** | `number` |  | [Defaults to `undefined`] |
| **version** | `number` |  | [Defaults to `undefined`] |

### Return type

**any**

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


## getResourceRawResourceIdGet

> MetadataResponse getResourceRawResourceIdGet(resourceId)

Get Resource

Return metadata for a single Raw layer resource.  Args:         resource_id (int): The id of the Raw resource.  Returns:         MetadataResponse: Resource id, name, description, project_id, and created_at.                 404 if not found.

### Example

```ts
import {
  Configuration,
  RawApi,
} from '';
import type { GetResourceRawResourceIdGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new RawApi();

  const body = {
    // number
    resourceId: 56,
  } satisfies GetResourceRawResourceIdGetRequest;

  try {
    const data = await api.getResourceRawResourceIdGet(body);
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
| **resourceId** | `number` |  | [Defaults to `undefined`] |

### Return type

[**MetadataResponse**](MetadataResponse.md)

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


## listResourcesRawGet

> Array&lt;MetadataResponse&gt; listResourcesRawGet()

List Resources

Return metadata for all Raw layer resources across all projects.  Returns:         list[MetadataResponse]: All Raw resources with id, name, description,                 project_id, and created_at.

### Example

```ts
import {
  Configuration,
  RawApi,
} from '';
import type { ListResourcesRawGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new RawApi();

  try {
    const data = await api.listResourcesRawGet();
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

[**Array&lt;MetadataResponse&gt;**](MetadataResponse.md)

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


## listVersionsRawResourceIdVersionsGet

> Array&lt;VersionResponse&gt; listVersionsRawResourceIdVersionsGet(resourceId)

List Versions

List all uploaded file versions for a Raw layer resource.  Args:         resource_id (int): The id of the Raw resource.  Returns:         list[VersionResponse]: Each entry contains id, resource_id, version (int),                 status (\&#39;active\&#39;/\&#39;inactive\&#39;), s3_key, created_at, and updated_at.

### Example

```ts
import {
  Configuration,
  RawApi,
} from '';
import type { ListVersionsRawResourceIdVersionsGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new RawApi();

  const body = {
    // number
    resourceId: 56,
  } satisfies ListVersionsRawResourceIdVersionsGetRequest;

  try {
    const data = await api.listVersionsRawResourceIdVersionsGet(body);
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
| **resourceId** | `number` |  | [Defaults to `undefined`] |

### Return type

[**Array&lt;VersionResponse&gt;**](VersionResponse.md)

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


## updateResourceRawResourceIdPatch

> MetadataResponse updateResourceRawResourceIdPatch(resourceId, updateResourceRequest)

Update Resource

Update the name and/or description of a Raw layer resource.  Args:         resource_id (int): The id of the Raw resource to update.         body (UpdateResourceRequest): name (str), description (str | None).  Returns:         MetadataResponse: Updated resource metadata. 404 if not found.

### Example

```ts
import {
  Configuration,
  RawApi,
} from '';
import type { UpdateResourceRawResourceIdPatchRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new RawApi();

  const body = {
    // number
    resourceId: 56,
    // UpdateResourceRequest
    updateResourceRequest: ...,
  } satisfies UpdateResourceRawResourceIdPatchRequest;

  try {
    const data = await api.updateResourceRawResourceIdPatch(body);
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
| **resourceId** | `number` |  | [Defaults to `undefined`] |
| **updateResourceRequest** | [UpdateResourceRequest](UpdateResourceRequest.md) |  | |

### Return type

[**MetadataResponse**](MetadataResponse.md)

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


## uploadVersionRawResourceIdVersionsPost

> MessageResponse uploadVersionRawResourceIdVersionsPost(resourceId, file)

Upload Version

Upload a new raw file as a new version of a Raw layer resource. Stored in S3; a version record is created in the database.  Args:         resource_id (int): The id of the Raw resource to upload to.         file (UploadFile): The raw file to upload.  Returns:         MessageResponse: Confirmation message.

### Example

```ts
import {
  Configuration,
  RawApi,
} from '';
import type { UploadVersionRawResourceIdVersionsPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new RawApi();

  const body = {
    // number
    resourceId: 56,
    // string
    file: file_example,
  } satisfies UploadVersionRawResourceIdVersionsPostRequest;

  try {
    const data = await api.uploadVersionRawResourceIdVersionsPost(body);
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
| **resourceId** | `number` |  | [Defaults to `undefined`] |
| **file** | `string` |  | [Defaults to `undefined`] |

### Return type

[**MessageResponse**](MessageResponse.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: `multipart/form-data`
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **201** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

