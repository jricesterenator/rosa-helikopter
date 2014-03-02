//package com.jjr.btcar.stream;
//
//import ErrorStreamReader;
//import StreamReader;
//import StreamWriter;
//
//import java.io.IOException;
//import java.io.InputStream;
//
//public class PythonProcess {
//
//    private final String filename;
////    private BufferedWriter os;
//    private Process process;
//    private InputStream inputStream;
//    private ErrorStreamReader errorStreamReader;
////    private StreamReader stdoutStreamReader;
//    private StreamWriter stdinWriter;
//
//    public PythonProcess(String filename) {
//        this.filename = filename;
//    }
//
//    public void executeInteractively() {
//        if(process != null) {
//            throw new IllegalStateException("Process is already active.");
//        }
//
//        try {
//
//            Runtime r = Runtime.getRuntime();
//            process = r.exec("python -i " + filename);
//
////            os = new BufferedWriter(new OutputStreamWriter(process.getOutputStream()));
//
//            inputStream = process.getInputStream();
//
//            errorStreamReader = new ErrorStreamReader(process.getErrorStream());
////            stdoutStreamReader = new StreamReader(process.getInputStream());
//            stdinWriter = new StreamWriter(process.getOutputStream());
//
//            Thread errorThread = new Thread(errorStreamReader);
//            errorThread.setDaemon(true);
//            errorThread.start();
////            new Thread(stdoutStreamReader).start();
//
//            Thread writerThread = new Thread(stdinWriter);
//            writerThread.setDaemon(true);
//            writerThread.start();
//
//        } catch (IOException e) {
//            throw new RuntimeException(e);
//        }
//    }
//
//    private String getStdout() {
//        checkProcess();
//
//        try {
//            //Print stdout
//            StringBuffer stdoutBuffer = new StringBuffer();
//            while (inputStream.available() == 0) {
//                Thread.yield();
//            }
//            while(inputStream.available() > 0) {
//                byte[] bytes = new byte[inputStream.available()];
//                inputStream.read(bytes);
//                stdoutBuffer.append(new String(bytes));
//            }
//            return stdoutBuffer.toString();
//
//        } catch (IOException e) {
//            throw new RuntimeException(e);
//        }
//    }
//
//    public String execute(String string) {
////        checkProcess();
//        return null;
////
////        StreamReader stdoutStreamReader = new StreamReader(process.getInputStream());
////        Thread thread = new Thread(stdoutStreamReader);
////        thread.start();
////
////        stdinWriter.write(string + "\n");
////        stdinWriter.flush();
////
////        while(thread.isAlive()) {
////            Thread.yield();
////        }
////
////        String output = stdoutStreamReader.getOutput().toString();
////        System.out.println("FOUND OUTPUT: " + output);
////
////        return output;
//    }
//
//
//    public StreamReader executeAsync(String string) {
//        return null;
////        checkProcess();
////
////        AsyncStreamReader stdoutStreamReader = new AsyncStreamReader(process.getInputStream());
////        Thread thread = new Thread(stdoutStreamReader);
////        stdoutStreamReader.setParentThread(thread);
////        thread.start();
////
////        stdinWriter.write(string + "\n");
////        stdinWriter.flush();
////
////        return stdoutStreamReader;
//
//    }
//
//    public void terminate() {
//        checkProcess();
//
//        process.destroy();
//        process = null;
//
//        errorStreamReader.kill();
//        stdinWriter.kill();
//    }
//
//    private void checkProcess() {
//        if(process == null) {
//            throw new IllegalStateException("Process is not active.");
//        }
//    }
//
//
//
//}
