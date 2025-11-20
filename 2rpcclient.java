import java.rmi.*;

public class Client {
    public static void main(String[] args) {
        try {
            RemoteExecutor exec = (RemoteExecutor) Naming.lookup("rmi://localhost/exec");

            System.out.println(exec.execute("add"));
            System.out.println(exec.execute("hello"));
            System.out.println(exec.execute("sort"));
            System.out.println(exec.execute("random"));

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
