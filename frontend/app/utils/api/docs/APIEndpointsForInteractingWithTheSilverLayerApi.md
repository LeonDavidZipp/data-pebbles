# APIEndpointsForInteractingWithTheSilverLayerApi

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**createResourceSilverPost**](APIEndpointsForInteractingWithTheSilverLayerApi.md#createresourcesilverpost) | **POST** /silver/ | Create Resource |
| [**deleteResourceSilverResourceIdDelete**](APIEndpointsForInteractingWithTheSilverLayerApi.md#deleteresourcesilverresourceiddelete) | **DELETE** /silver/{resource_id} | Delete Resource |
| [**downloadVersionSilverResourceIdVersionsVersionGet**](APIEndpointsForInteractingWithTheSilverLayerApi.md#downloadversionsilverresourceidversionsversionget) | **GET** /silver/{resource_id}/versions/{version} | Download Version |
| [**getResourceSilverResourceIdGet**](APIEndpointsForInteractingWithTheSilverLayerApi.md#getresourcesilverresourceidget) | **GET** /silver/{resource_id} | Get Resource |
| [**listResourcesSilverGet**](APIEndpointsForInteractingWithTheSilverLayerApi.md#listresourcessilverget) | **GET** /silver/ | List Resources |
| [**listVersionsSilverResourceIdVersionsGet**](APIEndpointsForInteractingWithTheSilverLayerApi.md#listversionssilverresourceidversionsget) | **GET** /silver/{resource_id}/versions | List Versions |
| [**updateResourceSilverResourceIdPatch**](APIEndpointsForInteractingWithTheSilverLayerApi.md#updateresourcesilverresourceidpatch) | **PATCH** /silver/{resource_id} | Update Resource |
| [**uploadVersionSilverResourceIdVersionsPost**](APIEndpointsForInteractingWithTheSilverLayerApi.md#uploadversionsilverresourceidversionspost) | **POST** /silver/{resource_id}/versions | Upload Version |



## createResourceSilverPost

> any createResourceSilverPost(createSilverResourceRequest)

Create Resource

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheSilverLayerApi,
} from '';
import type { CreateResourceSilverPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheSilverLayerApi();

  const body = {
    // CreateSilverResourceRequest
    createSilverResourceRequest: ...,
  } satisfies CreateResourceSilverPostRequest;

  try {
    const data = await api.createResourceSilverPost(body);
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
| **createSilverResourceRequest** | [CreateSilverResourceRequest](CreateSilverResourceRequest.md) |  | |

### Return type

**any**

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


## deleteResourceSilverResourceIdDelete

> any deleteResourceSilverResourceIdDelete(resourceId)

Delete Resource

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheSilverLayerApi,
} from '';
import type { DeleteResourceSilverResourceIdDeleteRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheSilverLayerApi();

  const body = {
    // number
    resourceId: 56,
  } satisfies DeleteResourceSilverResourceIdDeleteRequest;

  try {
    const data = await api.deleteResourceSilverResourceIdDelete(body);
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


## downloadVersionSilverResourceIdVersionsVersionGet

> any downloadVersionSilverResourceIdVersionsVersionGet(resourceId, version)

Download Version

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheSilverLayerApi,
} from '';
import type { DownloadVersionSilverResourceIdVersionsVersionGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheSilverLayerApi();

  const body = {
    // number
    resourceId: 56,
    // number
    version: 56,
  } satisfies DownloadVersionSilverResourceIdVersionsVersionGetRequest;

  try {
    const data = await api.downloadVersionSilverResourceIdVersionsVersionGet(body);
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


## getResourceSilverResourceIdGet

> SilverMetadataResponse getResourceSilverResourceIdGet(resourceId)

Get Resource

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheSilverLayerApi,
} from '';
import type { GetResourceSilverResourceIdGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheSilverLayerApi();

  const body = {
    // number
    resourceId: 56,
  } satisfies GetResourceSilverResourceIdGetRequest;

  try {
    const data = await api.getResourceSilverResourceIdGet(body);
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

[**SilverMetadataResponse**](SilverMetadataResponse.md)

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


## listResourcesSilverGet

> Array&lt;SilverMetadataResponse&gt; listResourcesSilverGet()

List Resources

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheSilverLayerApi,
} from '';
import type { ListResourcesSilverGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheSilverLayerApi();

  try {
    const data = await api.listResourcesSilverGet();
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

[**Array&lt;SilverMetadataResponse&gt;**](SilverMetadataResponse.md)

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


## listVersionsSilverResourceIdVersionsGet

> Array&lt;SilverLineageResponse&gt; listVersionsSilverResourceIdVersionsGet(resourceId)

List Versions

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheSilverLayerApi,
} from '';
import type { ListVersionsSilverResourceIdVersionsGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheSilverLayerApi();

  const body = {
    // number
    resourceId: 56,
  } satisfies ListVersionsSilverResourceIdVersionsGetRequest;

  try {
    const data = await api.listVersionsSilverResourceIdVersionsGet(body);
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

[**Array&lt;SilverLineageResponse&gt;**](SilverLineageResponse.md)

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


## updateResourceSilverResourceIdPatch

> SilverMetadataResponse updateResourceSilverResourceIdPatch(resourceId, updateSilverResourceRequest)

Update Resource

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheSilverLayerApi,
} from '';
import type { UpdateResourceSilverResourceIdPatchRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheSilverLayerApi();

  const body = {
    // number
    resourceId: 56,
    // UpdateSilverResourceRequest
    updateSilverResourceRequest: ...,
  } satisfies UpdateResourceSilverResourceIdPatchRequest;

  try {
    const data = await api.updateResourceSilverResourceIdPatch(body);
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
| **updateSilverResourceRequest** | [UpdateSilverResourceRequest](UpdateSilverResourceRequest.md) |  | |

### Return type

[**SilverMetadataResponse**](SilverMetadataResponse.md)

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


## uploadVersionSilverResourceIdVersionsPost

> any uploadVersionSilverResourceIdVersionsPost(resourceId, fromResourceId, file)

Upload Version

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheSilverLayerApi,
} from '';
import type { UploadVersionSilverResourceIdVersionsPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheSilverLayerApi();

  const body = {
    // number
    resourceId: 56,
    // number
    fromResourceId: 56,
    // string
    file: file_example,
  } satisfies UploadVersionSilverResourceIdVersionsPostRequest;

  try {
    const data = await api.uploadVersionSilverResourceIdVersionsPost(body);
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
| **fromResourceId** | `number` |  | [Defaults to `undefined`] |
| **file** | `string` |  | [Defaults to `undefined`] |

### Return type

**any**

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: `multipart/form-data`
- **Accept**: `application/json`


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
| **200** | Successful Response |  -  |
| **422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

