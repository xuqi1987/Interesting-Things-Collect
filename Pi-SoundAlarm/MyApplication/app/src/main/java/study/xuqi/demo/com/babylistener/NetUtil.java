package study.xuqi.demo.com.babylistener;

import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import org.json.JSONException;
import org.json.JSONObject;

/**
 * Created by xuqi on 16/3/14.
 */
public class NetUtil {

    public static final String DEF_CHATSET = "UTF-8";
    public static final int DEF_CONN_TIMEOUT = 30000;
    public static final int DEF_READ_TIMEOUT = 30000;
    public static String userAgent =  "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.66 Safari/537.36";

    //配置您申请的KEY
    public static final String APPKEY ="*************************";


    public static void test() {
        String result = null;
        String url = "http://120.24.161.10:8080/sound";
        Map params = new HashMap();//请求参数
        try  {
            result = net(url,params,"GET");
            Map data = toMap(result);
            System.out.println(data.get("id"));
            System.out.println(result);
        }catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static Map checkPi(String url) {
        System.out.println("checkPi " + url);
        String result = null;
        Map params = new HashMap();//请求参数
        Map data = new HashMap();
        try  {
            result = net(url,params,"GET");
            data = toMap(result);
        }catch (Exception e) {
            e.printStackTrace();
        }
        return data;
    }

    //1.基站定位
    public static void getRequest1(){
        String result =null;
        String url ="http://v.juhe.cn/cell/get";//请求接口地址
        Map params = new HashMap();//请求参数
        params.put("mnc","");//移动基站：0 联通基站:1  默认:0params.put("lac","");//小区号
        params.put("cell","");//基站号
        params.put("hex","");//进制类型，16或10，默认：10
        params.put("dtype","");//返回的数据格式：json/xml/jsonp
        params.put("callback","");//当选择jsonp格式时必须传递
        params.put("key",APPKEY);//APPKEY

        try {
            result =net(url, params, "GET");
            System.out.println(result);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }



    public static void main(String[] args) {

    }

    /**
     *
     * @param strUrl 请求地址
     * @param params 请求参数
     * @param method 请求方法
     * @return  网络请求字符串
     * @throws Exception
     */
    public static String net(String strUrl, Map params,String method) throws Exception {
        HttpURLConnection conn = null;
        BufferedReader reader = null;
        String rs = null;
        try {
            StringBuffer sb = new StringBuffer();
            if(method==null || method.equals("GET")){
                strUrl = strUrl+"?"+urlencode(params);
            }
            URL url = new URL(strUrl);
            conn = (HttpURLConnection) url.openConnection();
            if(method==null || method.equals("GET")){
                conn.setRequestMethod("GET");
            }else{
                conn.setRequestMethod("POST");
                conn.setDoOutput(true);
            }
            conn.setRequestProperty("User-agent", userAgent);
            conn.setUseCaches(false);
            conn.setConnectTimeout(DEF_CONN_TIMEOUT);
            conn.setReadTimeout(DEF_READ_TIMEOUT);
            conn.setInstanceFollowRedirects(false);
            conn.connect();
            if (params!= null && method.equals("POST")) {
                try {
                    DataOutputStream out = new DataOutputStream(conn.getOutputStream());
                    out.writeBytes(urlencode(params));
                } catch (Exception e) {
                    // TODO: handle exception
                }
            }
            InputStream is = conn.getInputStream();
            reader = new BufferedReader(new InputStreamReader(is, DEF_CHATSET));
            String strRead = null;
            while ((strRead = reader.readLine()) != null) {
                sb.append(strRead);
            }
            rs = sb.toString();
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (reader != null) {
                reader.close();
            }
            if (conn != null) {
                conn.disconnect();
            }
        }
        return rs;
    }

    //将map型转为请求参数型
    public static String urlencode(Map<String,Object>data) {
        StringBuilder sb = new StringBuilder();
        for (Map.Entry i : data.entrySet()) {
            try {
                sb.append(i.getKey()).append("=").append(URLEncoder.encode(i.getValue()+"","UTF-8")).append("&");
            } catch (UnsupportedEncodingException e) {
                e.printStackTrace();
            }
        }
        return sb.toString();
    }


    /**
     * 将Json对象转换成Map
     *
     * @return Map对象
     * @throws JSONException
     */
    public static Map toMap(String jsonString) throws JSONException {

        JSONObject jsonObject = new JSONObject(jsonString);

        Map result = new HashMap();
        Iterator iterator = jsonObject.keys();
        String key = null;
        String value = null;

        while (iterator.hasNext()) {

            key = (String) iterator.next();
            value = jsonObject.getString(key);
            result.put(key, value);

        }
        return result;

    }
}
