# APIEndpointsForInteractingWithTheSilverLayerApi

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**createResourceSilverPost**](APIEndpointsForInteractingWithTheSilverLayerApi.md#createresourcesilverpost) | **POST** /silver/ | Create Resource |
| [**deleteResourceSilverResourceIdDelete**](APIEndpointsForInteractingWithTheSilverLayerApi.md#deleteresourcesilverresourceiddelete) | **DELETE** /silver/{resource_id} | Delete Resource |
| [**downloadVersionSilverResourceIdVersionsVersionGet**](APIEndpointsForInteractingWithTheSilverLayerApi.md#downloadversionsilverresourceidversionsversionget) | **GET** /silver/{resource_id}/versions/{version} | Download Version |
| [**getResourceSilverResourceIdGet**](APIEndpointsForInteractingWithTheSilverLayerApi.md#getresourcesilverresourceidget) | **GET** /silver/{resource_id} | Get Resource |
| [**getSchemaSilverResourceIdVersionsVersionSchemaGet**](APIEndpointsForInteractingWithTheSilverLayerApi.md#getschemasilverresourceidversionsversionschemaget) | **GET** /silver/{resource_id}/versions/{version}/schema | Get Schema |
| [**listResourcesSilverGet**](APIEndpointsForInteractingWithTheSilverLayerApi.md#listresourcessilverget) | **GET** /silver/ | List Resources |
| [**listVersionsSilverResourceIdVersionsGet**](APIEndpointsForInteractingWithTheSilverLayerApi.md#listversionssilverresourceidversionsget) | **GET** /silver/{resource_id}/versions | List Versions |
| [**updateResourceSilverResourceIdPatch**](APIEndpointsForInteractingWithTheSilverLayerApi.md#updateresourcesilverresourceidpatch) | **PATCH** /silver/{resource_id} | Update Resource |
| [**uploadVersionSingleSilverResourceIdVersionsPost**](APIEndpointsForInteractingWithTheSilverLayerApi.md#uploadversionsinglesilverresourceidversionspost) | **POST** /silver/{resource_id}/versions | Upload Version Single |



## createResourceSilverPost

> CreateResourceResponse createResourceSilverPost(createResourceRequest)

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
    // CreateResourceRequest
    createResourceRequest: ...,
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


## deleteResourceSilverResourceIdDelete

> MessageResponse deleteResourceSilverResourceIdDelete(resourceId)

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

> MetadataResponse getResourceSilverResourceIdGet(resourceId)

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


## getSchemaSilverResourceIdVersionsVersionSchemaGet

> SchemaResponse getSchemaSilverResourceIdVersionsVersionSchemaGet(resourceId, version)

Get Schema

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheSilverLayerApi,
} from '';
import type { GetSchemaSilverResourceIdVersionsVersionSchemaGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheSilverLayerApi();

  const body = {
    // number
    resourceId: 56,
    // number
    version: 56,
  } satisfies GetSchemaSilverResourceIdVersionsVersionSchemaGetRequest;

  try {
    const data = await api.getSchemaSilverResourceIdVersionsVersionSchemaGet(body);
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

[**SchemaResponse**](SchemaResponse.md)

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

> Array&lt;MetadataResponse&gt; listResourcesSilverGet()

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


## listVersionsSilverResourceIdVersionsGet

> Array&lt;LineageResponse&gt; listVersionsSilverResourceIdVersionsGet(resourceId)

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

[**Array&lt;LineageResponse&gt;**](LineageResponse.md)

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

> MetadataResponse updateResourceSilverResourceIdPatch(resourceId, updateResourceRequest)

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
    // UpdateResourceRequest
    updateResourceRequest: ...,
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


## uploadVersionSingleSilverResourceIdVersionsPost

> MessageResponse uploadVersionSingleSilverResourceIdVersionsPost(resourceId, fromResourceId, file)

Upload Version Single

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheSilverLayerApi,
} from '';
import type { UploadVersionSingleSilverResourceIdVersionsPostRequest } from '';

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
  } satisfies UploadVersionSingleSilverResourceIdVersionsPostRequest;

  try {
    const data = await api.uploadVersionSingleSilverResourceIdVersionsPost(body);
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

