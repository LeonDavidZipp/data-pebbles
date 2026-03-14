# APIEndpointsForInteractingWithTheGoldLayerApi

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
|------------- | ------------- | -------------|
| [**createSourceGoldPost**](APIEndpointsForInteractingWithTheGoldLayerApi.md#createsourcegoldpost) | **POST** /gold/ | Create Source |
| [**deleteSourceGoldSourceIdDelete**](APIEndpointsForInteractingWithTheGoldLayerApi.md#deletesourcegoldsourceiddelete) | **DELETE** /gold/{source_id} | Delete Source |
| [**downloadVersionGoldSourceIdVersionsVersionGet**](APIEndpointsForInteractingWithTheGoldLayerApi.md#downloadversiongoldsourceidversionsversionget) | **GET** /gold/{source_id}/versions/{version} | Download Version |
| [**getSourceGoldSourceIdGet**](APIEndpointsForInteractingWithTheGoldLayerApi.md#getsourcegoldsourceidget) | **GET** /gold/{source_id} | Get Source |
| [**listSourcesGoldGet**](APIEndpointsForInteractingWithTheGoldLayerApi.md#listsourcesgoldget) | **GET** /gold/ | List Sources |
| [**listVersionsGoldSourceIdVersionsGet**](APIEndpointsForInteractingWithTheGoldLayerApi.md#listversionsgoldsourceidversionsget) | **GET** /gold/{source_id}/versions | List Versions |
| [**updateSourceGoldSourceIdPatch**](APIEndpointsForInteractingWithTheGoldLayerApi.md#updatesourcegoldsourceidpatch) | **PATCH** /gold/{source_id} | Update Source |
| [**uploadVersionGoldSourceIdVersionsPost**](APIEndpointsForInteractingWithTheGoldLayerApi.md#uploadversiongoldsourceidversionspost) | **POST** /gold/{source_id}/versions | Upload Version |



## createSourceGoldPost

> any createSourceGoldPost(createGoldSourceRequest)

Create Source

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheGoldLayerApi,
} from '';
import type { CreateSourceGoldPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheGoldLayerApi();

  const body = {
    // CreateGoldSourceRequest
    createGoldSourceRequest: ...,
  } satisfies CreateSourceGoldPostRequest;

  try {
    const data = await api.createSourceGoldPost(body);
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
| **createGoldSourceRequest** | [CreateGoldSourceRequest](CreateGoldSourceRequest.md) |  | |

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


## deleteSourceGoldSourceIdDelete

> any deleteSourceGoldSourceIdDelete(sourceId)

Delete Source

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheGoldLayerApi,
} from '';
import type { DeleteSourceGoldSourceIdDeleteRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheGoldLayerApi();

  const body = {
    // number
    sourceId: 56,
  } satisfies DeleteSourceGoldSourceIdDeleteRequest;

  try {
    const data = await api.deleteSourceGoldSourceIdDelete(body);
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
| **sourceId** | `number` |  | [Defaults to `undefined`] |

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


## downloadVersionGoldSourceIdVersionsVersionGet

> any downloadVersionGoldSourceIdVersionsVersionGet(sourceId, version)

Download Version

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheGoldLayerApi,
} from '';
import type { DownloadVersionGoldSourceIdVersionsVersionGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheGoldLayerApi();

  const body = {
    // number
    sourceId: 56,
    // number
    version: 56,
  } satisfies DownloadVersionGoldSourceIdVersionsVersionGetRequest;

  try {
    const data = await api.downloadVersionGoldSourceIdVersionsVersionGet(body);
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
| **sourceId** | `number` |  | [Defaults to `undefined`] |
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


## getSourceGoldSourceIdGet

> GoldMetadataResponse getSourceGoldSourceIdGet(sourceId)

Get Source

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheGoldLayerApi,
} from '';
import type { GetSourceGoldSourceIdGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheGoldLayerApi();

  const body = {
    // number
    sourceId: 56,
  } satisfies GetSourceGoldSourceIdGetRequest;

  try {
    const data = await api.getSourceGoldSourceIdGet(body);
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
| **sourceId** | `number` |  | [Defaults to `undefined`] |

### Return type

[**GoldMetadataResponse**](GoldMetadataResponse.md)

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


## listSourcesGoldGet

> Array&lt;GoldMetadataResponse&gt; listSourcesGoldGet()

List Sources

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheGoldLayerApi,
} from '';
import type { ListSourcesGoldGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheGoldLayerApi();

  try {
    const data = await api.listSourcesGoldGet();
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

[**Array&lt;GoldMetadataResponse&gt;**](GoldMetadataResponse.md)

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


## listVersionsGoldSourceIdVersionsGet

> Array&lt;GoldLineageResponse&gt; listVersionsGoldSourceIdVersionsGet(sourceId)

List Versions

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheGoldLayerApi,
} from '';
import type { ListVersionsGoldSourceIdVersionsGetRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheGoldLayerApi();

  const body = {
    // number
    sourceId: 56,
  } satisfies ListVersionsGoldSourceIdVersionsGetRequest;

  try {
    const data = await api.listVersionsGoldSourceIdVersionsGet(body);
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
| **sourceId** | `number` |  | [Defaults to `undefined`] |

### Return type

[**Array&lt;GoldLineageResponse&gt;**](GoldLineageResponse.md)

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


## updateSourceGoldSourceIdPatch

> GoldMetadataResponse updateSourceGoldSourceIdPatch(sourceId, updateGoldSourceRequest)

Update Source

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheGoldLayerApi,
} from '';
import type { UpdateSourceGoldSourceIdPatchRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheGoldLayerApi();

  const body = {
    // number
    sourceId: 56,
    // UpdateGoldSourceRequest
    updateGoldSourceRequest: ...,
  } satisfies UpdateSourceGoldSourceIdPatchRequest;

  try {
    const data = await api.updateSourceGoldSourceIdPatch(body);
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
| **sourceId** | `number` |  | [Defaults to `undefined`] |
| **updateGoldSourceRequest** | [UpdateGoldSourceRequest](UpdateGoldSourceRequest.md) |  | |

### Return type

[**GoldMetadataResponse**](GoldMetadataResponse.md)

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


## uploadVersionGoldSourceIdVersionsPost

> any uploadVersionGoldSourceIdVersionsPost(sourceId, sources, file)

Upload Version

### Example

```ts
import {
  Configuration,
  APIEndpointsForInteractingWithTheGoldLayerApi,
} from '';
import type { UploadVersionGoldSourceIdVersionsPostRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new APIEndpointsForInteractingWithTheGoldLayerApi();

  const body = {
    // number
    sourceId: 56,
    // Array<number>
    sources: ...,
    // string
    file: file_example,
  } satisfies UploadVersionGoldSourceIdVersionsPostRequest;

  try {
    const data = await api.uploadVersionGoldSourceIdVersionsPost(body);
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
| **sourceId** | `number` |  | [Defaults to `undefined`] |
| **sources** | `Array<number>` |  | |
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

