# APIEndpointsForInteractingWithTheBronzeLayerApi

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**activateVersionBronzeResourceIdVersionsVersionPatch**](APIEndpointsForInteractingWithTheBronzeLayerApi.md#activateversionbronzeresourceidversionsversionpatch) | **PATCH** /bronze/{resource_id}/versions/{version} | Activate Version |
| [**createResourceBronzePost**](APIEndpointsForInteractingWithTheBronzeLayerApi.md#createresourcebronzepost) | **POST** /bronze/ | Create Resource |
| [**deleteResourceBronzeResourceIdDelete**](APIEndpointsForInteractingWithTheBronzeLayerApi.md#deleteresourcebronzeresourceiddelete) | **DELETE** /bronze/{resource_id} | Delete Resource |
| [**deleteVersionBronzeResourceIdVersionsVersionDelete**](APIEndpointsForInteractingWithTheBronzeLayerApi.md#deleteversionbronzeresourceidversionsversiondelete) | **DELETE** /bronze/{resource_id}/versions/{version} | Delete Version |
| [**downloadVersionBronzeResourceIdVersionsVersionGet**](APIEndpointsForInteractingWithTheBronzeLayerApi.md#downloadversionbronzeresourceidversionsversionget) | **GET** /bronze/{resource_id}/versions/{version} | Download Version |
| [**getResourceBronzeResourceIdGet**](APIEndpointsForInteractingWithTheBronzeLayerApi.md#getresourcebronzeresourceidget) | **GET** /bronze/{resource_id} | Get Resource |
| [**listResourcesBronzeGet**](APIEndpointsForInteractingWithTheBronzeLayerApi.md#listresourcesbronzeget) | **GET** /bronze/ | List Resources |
| [**listVersionsBronzeResourceIdVersionsGet**](APIEndpointsForInteractingWithTheBronzeLayerApi.md#listversionsbronzeresourceidversionsget) | **GET** /bronze/{resource_id}/versions | List Versions |
| [**updateResourceBronzeResourceIdPatch**](APIEndpointsForInteractingWithTheBronzeLayerApi.md#updateresourcebronzeresourceidpatch) | **PATCH** /bronze/{resource_id} | Update Resource |
| [**uploadVersionBronzeResourceIdVersionsPost**](APIEndpointsForInteractingWithTheBronzeLayerApi.md#uploadversionbronzeresourceidversionspost) | **POST** /bronze/{resource_id}/versions | Upload Version |



## activateVersionBronzeResourceIdVersionsVersionPatch

> MessageResponse activateVersionBronzeResourceIdVersionsVersionPatch(resourceId, version)

Activate Version

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheBronzeLayerApi,
} from '';
import type { ActivateVersionBronzeResourceIdVersionsVersionPatchRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheBronzeLayerApi();

  const body = {
    // number
    resourceId: 56,
    // number
    version: 56,
  } satisfies ActivateVersionBronzeResourceIdVersionsVersionPatchRequest;

  try {
    const data = await api.activateVersionBronzeResourceIdVersionsVersionPatch(body);
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


## createResourceBronzePost

> CreateResourceResponse createResourceBronzePost(createResourceRequest)

Create Resource

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheBronzeLayerApi,
} from '';
import type { CreateResourceBronzePostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheBronzeLayerApi();

  const body = {
    // CreateResourceRequest
    createResourceRequest: ...,
  } satisfies CreateResourceBronzePostRequest;

  try {
    const data = await api.createResourceBronzePost(body);
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


## deleteResourceBronzeResourceIdDelete

> MessageResponse deleteResourceBronzeResourceIdDelete(resourceId)

Delete Resource

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheBronzeLayerApi,
} from '';
import type { DeleteResourceBronzeResourceIdDeleteRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheBronzeLayerApi();

  const body = {
    // number
    resourceId: 56,
  } satisfies DeleteResourceBronzeResourceIdDeleteRequest;

  try {
    const data = await api.deleteResourceBronzeResourceIdDelete(body);
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


## deleteVersionBronzeResourceIdVersionsVersionDelete

> MessageResponse deleteVersionBronzeResourceIdVersionsVersionDelete(resourceId, version)

Delete Version

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheBronzeLayerApi,
} from '';
import type { DeleteVersionBronzeResourceIdVersionsVersionDeleteRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheBronzeLayerApi();

  const body = {
    // number
    resourceId: 56,
    // number
    version: 56,
  } satisfies DeleteVersionBronzeResourceIdVersionsVersionDeleteRequest;

  try {
    const data = await api.deleteVersionBronzeResourceIdVersionsVersionDelete(body);
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


## downloadVersionBronzeResourceIdVersionsVersionGet

> any downloadVersionBronzeResourceIdVersionsVersionGet(resourceId, version)

Download Version

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheBronzeLayerApi,
} from '';
import type { DownloadVersionBronzeResourceIdVersionsVersionGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheBronzeLayerApi();

  const body = {
    // number
    resourceId: 56,
    // number
    version: 56,
  } satisfies DownloadVersionBronzeResourceIdVersionsVersionGetRequest;

  try {
    const data = await api.downloadVersionBronzeResourceIdVersionsVersionGet(body);
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


## getResourceBronzeResourceIdGet

> MetadataResponse getResourceBronzeResourceIdGet(resourceId)

Get Resource

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheBronzeLayerApi,
} from '';
import type { GetResourceBronzeResourceIdGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheBronzeLayerApi();

  const body = {
    // number
    resourceId: 56,
  } satisfies GetResourceBronzeResourceIdGetRequest;

  try {
    const data = await api.getResourceBronzeResourceIdGet(body);
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


## listResourcesBronzeGet

> Array&lt;MetadataResponse&gt; listResourcesBronzeGet()

List Resources

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheBronzeLayerApi,
} from '';
import type { ListResourcesBronzeGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheBronzeLayerApi();

  try {
    const data = await api.listResourcesBronzeGet();
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


## listVersionsBronzeResourceIdVersionsGet

> Array&lt;VersionResponse&gt; listVersionsBronzeResourceIdVersionsGet(resourceId)

List Versions

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheBronzeLayerApi,
} from '';
import type { ListVersionsBronzeResourceIdVersionsGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheBronzeLayerApi();

  const body = {
    // number
    resourceId: 56,
  } satisfies ListVersionsBronzeResourceIdVersionsGetRequest;

  try {
    const data = await api.listVersionsBronzeResourceIdVersionsGet(body);
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


## updateResourceBronzeResourceIdPatch

> MetadataResponse updateResourceBronzeResourceIdPatch(resourceId, updateResourceRequest)

Update Resource

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheBronzeLayerApi,
} from '';
import type { UpdateResourceBronzeResourceIdPatchRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheBronzeLayerApi();

  const body = {
    // number
    resourceId: 56,
    // UpdateResourceRequest
    updateResourceRequest: ...,
  } satisfies UpdateResourceBronzeResourceIdPatchRequest;

  try {
    const data = await api.updateResourceBronzeResourceIdPatch(body);
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


## uploadVersionBronzeResourceIdVersionsPost

> MessageResponse uploadVersionBronzeResourceIdVersionsPost(resourceId, file)

Upload Version

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheBronzeLayerApi,
} from '';
import type { UploadVersionBronzeResourceIdVersionsPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheBronzeLayerApi();

  const body = {
    // number
    resourceId: 56,
    // string
    file: file_example,
  } satisfies UploadVersionBronzeResourceIdVersionsPostRequest;

  try {
    const data = await api.uploadVersionBronzeResourceIdVersionsPost(body);
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

