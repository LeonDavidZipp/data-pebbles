# APIEndpointsForInteractingWithTheGoldLayerApi

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**createResourceGoldPost**](APIEndpointsForInteractingWithTheGoldLayerApi.md#createresourcegoldpost) | **POST** /gold/ | Create Resource |
| [**deleteResourceGoldResourceIdDelete**](APIEndpointsForInteractingWithTheGoldLayerApi.md#deleteresourcegoldresourceiddelete) | **DELETE** /gold/{resource_id} | Delete Resource |
| [**downloadVersionGoldResourceIdVersionsVersionGet**](APIEndpointsForInteractingWithTheGoldLayerApi.md#downloadversiongoldresourceidversionsversionget) | **GET** /gold/{resource_id}/versions/{version} | Download Version |
| [**getResourceGoldResourceIdGet**](APIEndpointsForInteractingWithTheGoldLayerApi.md#getresourcegoldresourceidget) | **GET** /gold/{resource_id} | Get Resource |
| [**getSchemaGoldResourceIdVersionsVersionSchemaGet**](APIEndpointsForInteractingWithTheGoldLayerApi.md#getschemagoldresourceidversionsversionschemaget) | **GET** /gold/{resource_id}/versions/{version}/schema | Get Schema |
| [**listResourcesGoldGet**](APIEndpointsForInteractingWithTheGoldLayerApi.md#listresourcesgoldget) | **GET** /gold/ | List Resources |
| [**listVersionsGoldResourceIdVersionsGet**](APIEndpointsForInteractingWithTheGoldLayerApi.md#listversionsgoldresourceidversionsget) | **GET** /gold/{resource_id}/versions | List Versions |
| [**updateResourceGoldResourceIdPatch**](APIEndpointsForInteractingWithTheGoldLayerApi.md#updateresourcegoldresourceidpatch) | **PATCH** /gold/{resource_id} | Update Resource |
| [**uploadVersionMultiGoldResourceIdVersionsPost**](APIEndpointsForInteractingWithTheGoldLayerApi.md#uploadversionmultigoldresourceidversionspost) | **POST** /gold/{resource_id}/versions | Upload Version Multi |



## createResourceGoldPost

> CreateResourceResponse createResourceGoldPost(createResourceRequest)

Create Resource

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheGoldLayerApi,
} from '';
import type { CreateResourceGoldPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheGoldLayerApi();

  const body = {
    // CreateResourceRequest
    createResourceRequest: ...,
  } satisfies CreateResourceGoldPostRequest;

  try {
    const data = await api.createResourceGoldPost(body);
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


## deleteResourceGoldResourceIdDelete

> MessageResponse deleteResourceGoldResourceIdDelete(resourceId)

Delete Resource

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheGoldLayerApi,
} from '';
import type { DeleteResourceGoldResourceIdDeleteRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheGoldLayerApi();

  const body = {
    // number
    resourceId: 56,
  } satisfies DeleteResourceGoldResourceIdDeleteRequest;

  try {
    const data = await api.deleteResourceGoldResourceIdDelete(body);
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


## downloadVersionGoldResourceIdVersionsVersionGet

> any downloadVersionGoldResourceIdVersionsVersionGet(resourceId, version)

Download Version

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheGoldLayerApi,
} from '';
import type { DownloadVersionGoldResourceIdVersionsVersionGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheGoldLayerApi();

  const body = {
    // number
    resourceId: 56,
    // number
    version: 56,
  } satisfies DownloadVersionGoldResourceIdVersionsVersionGetRequest;

  try {
    const data = await api.downloadVersionGoldResourceIdVersionsVersionGet(body);
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


## getResourceGoldResourceIdGet

> MetadataResponse getResourceGoldResourceIdGet(resourceId)

Get Resource

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheGoldLayerApi,
} from '';
import type { GetResourceGoldResourceIdGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheGoldLayerApi();

  const body = {
    // number
    resourceId: 56,
  } satisfies GetResourceGoldResourceIdGetRequest;

  try {
    const data = await api.getResourceGoldResourceIdGet(body);
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


## getSchemaGoldResourceIdVersionsVersionSchemaGet

> SchemaResponse getSchemaGoldResourceIdVersionsVersionSchemaGet(resourceId, version)

Get Schema

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheGoldLayerApi,
} from '';
import type { GetSchemaGoldResourceIdVersionsVersionSchemaGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheGoldLayerApi();

  const body = {
    // number
    resourceId: 56,
    // number
    version: 56,
  } satisfies GetSchemaGoldResourceIdVersionsVersionSchemaGetRequest;

  try {
    const data = await api.getSchemaGoldResourceIdVersionsVersionSchemaGet(body);
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


## listResourcesGoldGet

> Array&lt;MetadataResponse&gt; listResourcesGoldGet()

List Resources

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheGoldLayerApi,
} from '';
import type { ListResourcesGoldGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheGoldLayerApi();

  try {
    const data = await api.listResourcesGoldGet();
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


## listVersionsGoldResourceIdVersionsGet

> Array&lt;LineageResponse&gt; listVersionsGoldResourceIdVersionsGet(resourceId)

List Versions

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheGoldLayerApi,
} from '';
import type { ListVersionsGoldResourceIdVersionsGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheGoldLayerApi();

  const body = {
    // number
    resourceId: 56,
  } satisfies ListVersionsGoldResourceIdVersionsGetRequest;

  try {
    const data = await api.listVersionsGoldResourceIdVersionsGet(body);
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


## updateResourceGoldResourceIdPatch

> MetadataResponse updateResourceGoldResourceIdPatch(resourceId, updateResourceRequest)

Update Resource

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheGoldLayerApi,
} from '';
import type { UpdateResourceGoldResourceIdPatchRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheGoldLayerApi();

  const body = {
    // number
    resourceId: 56,
    // UpdateResourceRequest
    updateResourceRequest: ...,
  } satisfies UpdateResourceGoldResourceIdPatchRequest;

  try {
    const data = await api.updateResourceGoldResourceIdPatch(body);
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


## uploadVersionMultiGoldResourceIdVersionsPost

> MessageResponse uploadVersionMultiGoldResourceIdVersionsPost(resourceId, resources, file)

Upload Version Multi

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheGoldLayerApi,
} from '';
import type { UploadVersionMultiGoldResourceIdVersionsPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheGoldLayerApi();

  const body = {
    // number
    resourceId: 56,
    // Array<number>
    resources: ...,
    // string
    file: file_example,
  } satisfies UploadVersionMultiGoldResourceIdVersionsPostRequest;

  try {
    const data = await api.uploadVersionMultiGoldResourceIdVersionsPost(body);
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
| **resources** | `Array<number>` |  | |
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

