//package com.jjr.btcar.stream;
//
//import java.io.IOException;
//import java.io.InputStream;
//
//public class StreamReader implements Runnable
//{
//    protected InputStream in;
//    protected StringBuffer outputBuffer = new StringBuffer();
//    protected Thread parentThread;
//
//    public StreamReader(InputStream in)
//    {
//        this.in = in;
//    }
//
//    public void run ()
//    {
//        byte[] buffer = new byte[1024];
//        int len = -1;
//        try
//        {
//            //Wait for some output
//            while(in.available() == 0) {
//                Thread.yield();
//            }
//            //Read all of the output
//            while ( in.available() > 0 && ( len = this.in.read(buffer)) > -1 )
//            {
//                String string = new String(buffer, 0, len);
//                outputBuffer.append(string);
//            }
//
//        }
//        catch ( IOException e ) {
//            e.printStackTrace();
//        }
//
//    }
//
//
//    public StringBuffer getOutput() {
//        return outputBuffer;
//    }
//
//    public void setParentThread(Thread parentThread) {
//        this.parentThread = parentThread;
//    }
//
//    public Thread getParentThread() {
//        return parentThread;
//    }
//}
//
