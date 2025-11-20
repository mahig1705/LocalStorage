import java.rmi.*;
import java.rmi.registry.*;
import java.rmi.server.*;
import java.util.concurrent.*;

interface RemoteExecutor extends Remote {
    String execute(String code) throws RemoteException;
}

class RemoteExecutorImpl extends UnicastRemoteObject implements RemoteExecutor {
    private final ExecutorService pool = Executors.newFixedThreadPool(10);

    protected RemoteExecutorImpl() throws RemoteException { super(); }

    public String execute(String code) throws RemoteException {
        Callable<String> task = () -> {
            switch (code.toLowerCase()) {
                case "add": return "5 + 7 = " + (5+7);
                case "sort": return "Sorted: [1, 2, 3, 5, 7]";
                case "hello": return "Hello from Server!";
                default: return "Unknown task: " + code;
            }
        };

        try { return pool.submit(task).get(); }
        catch (Exception e) { throw new RemoteException("Task failed", e); }
    }
}

public class Server {
    public static void main(String[] args) {
        try {
            LocateRegistry.createRegistry(1099);
            RemoteExecutor exec = new RemoteExecutorImpl();
            Naming.rebind("rmi://localhost/exec", exec);
            System.out.println("Server Ready...");
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
