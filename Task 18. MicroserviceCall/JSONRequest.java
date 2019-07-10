package com.nathansizemore;

import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.HttpClientBuilder;
import org.apache.http.message.BasicHeader;
import org.apache.http.protocol.HTTP;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.URLEncoder;


public abstract class JSONRequest {

    /*
     * Called once response has been received and parsed.
     *
     * @param   json    The {@link JSONObject} that is returned back
     */
    public abstract void onResponse(JSONObject json);

    /*
     * Called upon any error in the process
     *
     * @param   msg  The error msg
     * @param   e    The {@link Exception} that was thrown (Can be null)
     */
    public abstract void onError(String msg, Exception e);

    /*
     * Called to begin the process
     *
     * @param   type    Type of request, can be "POST" or "GET" (case insensitive)
     * @param   url     URL to send request to.
     * @param   json    The {@link JSONObject} to send, null if not needed
     */
    public final void makeRequest(String type, String url, JSONObject json) {
        if (type.equalsIgnoreCase("GET")) {
            if (json == null) {
                getRequest(url);
            } else {
                getRequest(url, json);
            }
        } else if (type.equalsIgnoreCase("POST")) {
            postRequest(url, json);
        } else {
            onError("Expects parameter type to be GET or POST", null);
        }
    }

    /*
     * Starts a new thread for a GET Request
     *
     * @param   url     URL to send request to.
     * @param   json    The {@link JSONObject} to send
     */
    private void getRequest(String url, JSONObject json) {
        Thread thread = new Thread(new GetRequest(url, json));
        thread.start();
    }

    /*
     * Starts a new thread for a GET Request
     *
     * @param   url     URL to send request to.
     */
    private void getRequest(String url) {
        Thread thread = new Thread(new GetRequest(url));
        thread.start();
    }

    /*
     * Starts a new thread for a POST Request
     *
     * @param   url     URL to send request to.
     * @param   json    The {@link JSONObject} to send
     */
    private void postRequest(String url, JSONObject json) {
        Thread thread = new Thread(new PostRequest(url, json));
        thread.start();
    }

    /*
     * New thread for a GET Request
     */
    private final class GetRequest implements Runnable {
        private String url;
        private JSONObject json;

        public GetRequest(String url) {
            this.url = url;
            this.json = null;
        }

        public GetRequest(String url, JSONObject json) {
            this.url = url;
            this.json = json;
        }

        @Override
        public void run() {
            try {
                HttpClient httpClient = HttpClientBuilder.create().build();
                HttpGet httpGet = new HttpGet(url);
                if (json != null) {
                    String encodedUrl = url + URLEncoder.encode(json.toString(), "UTF-8");
                    httpGet = new HttpGet(encodedUrl);
                }
                HttpResponse response = httpClient.execute(httpGet);

                if (response != null) {
                    InputStream in = response.getEntity().getContent();
                    BufferedReader streamReader = new BufferedReader(new InputStreamReader(in, "UTF-8"));
                    StringBuilder responseStrBuilder = new StringBuilder();
                    String inputStr;
                    while ((inputStr = streamReader.readLine()) != null) {
                        responseStrBuilder.append(inputStr);
                    }
                    JSONObject jsonResponse = new JSONObject(responseStrBuilder.toString());
                    onResponse(jsonResponse);
                } else {
                    onError("Response was null", null);
                }
            } catch (Exception e) {
                onError(e.getMessage(), e);
            }
        }
    }

    /*
     * New thread for a POST Request
     */
    private final class PostRequest implements Runnable {
        private String url;
        private JSONObject json;

        public PostRequest(String url, JSONObject json) {
            this.url = url;
            this.json = json;
        }

        @Override
        public void run() {
            try {
                HttpClient httpClient = HttpClientBuilder.create().build();
                StringEntity params = new StringEntity(json.toString());
                params.setContentType(new BasicHeader(HTTP.CONTENT_TYPE, "application/json"));
                HttpPost httpPost = new HttpPost(url);
                httpPost.setEntity(params);
                HttpResponse response = httpClient.execute(httpPost);

                if (response != null) {
                    InputStream in = response.getEntity().getContent();
                    BufferedReader streamReader = new BufferedReader(new InputStreamReader(in, "UTF-8"));
                    StringBuilder responseStrBuilder = new StringBuilder();
                    String inputStr;
                    while ((inputStr = streamReader.readLine()) != null) {
                        responseStrBuilder.append(inputStr);
                    }
                    JSONObject jsonResponse = new JSONObject(responseStrBuilder.toString());
                    onResponse(jsonResponse);
                } else {
                    onError("Response was null", null);
                }
            } catch (Exception e) {
                onError(e.getMessage(), e);
            }
        }
    }
}
