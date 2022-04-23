package study.xuqi.demo.com.babylistener;

import android.app.Service;
import android.content.Intent;
import android.media.MediaPlayer;
import android.os.IBinder;

import java.util.Map;

public class CheckStateService extends Service {
    private boolean isRunning = false;
    private MediaPlayer mp =null;
    private String url = "";
    private boolean playsound = false;
    public CheckStateService() {
    }

    @Override
    public IBinder onBind(Intent intent) {
        System.out.println("绑定");
        url = intent.getExtras().getString("msg");
        return new Binder();
    }

    public class Binder extends android.os.Binder {
        public void setData(String data) {
            System.out.println("Binder 设置数据");
        }

        public void stopplay(){
            CheckStateService.this.stopSound();
        }

        public void play() {
            CheckStateService.this.playSound();
        }


    }

    @Override
    public void onCreate() {
        System.out.println("onCreate");
        isRunning = true;

        super.onCreate();
    }


    @Override
    public boolean onUnbind(Intent intent) {
        return super.onUnbind(intent);
    }

    @Override
    public void onDestroy() {
        System.out.println("onDestory");
        isRunning = false;
        super.onDestroy();
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        System.out.println("onStartCommand");
        new Thread() {
            @Override
            public void run() {
                super.run();
                int i =0;
                while(isRunning) {
                    i++;

                    Map map = NetUtil.checkPi(url);

                    String st = map.get("id").toString();
                    if (st.equals("true")) {
                        if (!playsound) {
                            playSound();
                            playsound = true;
                        }
                    } else {
                        stopSound();
                        playsound = false;
                    }

                    //System.out.println("hello");
                    try {
                        sleep(3000);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }

                }


            }
        }.start();
        return super.onStartCommand(intent, flags, startId);
    }

    private void playSound(){
        System.out.println("Play");
        if(mp != null) {
            mp.reset();
        }


        mp = MediaPlayer.create(this, R.raw.cry);

        try {
            //mp.prepare();
            mp.start();
        } catch (IllegalArgumentException e) {
            e.printStackTrace();
        } catch (IllegalStateException e) {
            e.printStackTrace();
        }
        mp.setOnCompletionListener(new MediaPlayer.OnCompletionListener() {
            @Override
            public void onCompletion(MediaPlayer mp) {
                mp.release();
            }
        });
    }

    private void stopSound(){
        System.out.println("stop");
        if(mp !=null) {
            mp.stop();

        }
    }

}
