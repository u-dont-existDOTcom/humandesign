using System;
using System.Text;
using System.Runtime.InteropServices;
using System.Diagnostics;
using System.Drawing;
using System.Drawing.Imaging;

// Bounded operator for an already running Mastro process. No unrelated windows.
class WineControls {
  delegate bool EnumProc(IntPtr hwnd, IntPtr data);
  [DllImport("user32.dll")] static extern bool EnumWindows(EnumProc cb, IntPtr data);
  [DllImport("user32.dll")] static extern bool EnumChildWindows(IntPtr h, EnumProc cb, IntPtr data);
  [DllImport("user32.dll")] static extern uint GetWindowThreadProcessId(IntPtr h, out uint pid);
  [DllImport("user32.dll", CharSet=CharSet.Unicode)] static extern int GetWindowText(IntPtr h, StringBuilder b, int n);
  [DllImport("user32.dll", CharSet=CharSet.Unicode)] static extern int GetClassName(IntPtr h, StringBuilder b, int n);
  [DllImport("user32.dll")] static extern bool IsWindowVisible(IntPtr h);
  [DllImport("user32.dll")] static extern bool IsWindowEnabled(IntPtr h);
  [DllImport("user32.dll")] static extern bool GetWindowRect(IntPtr h, out Rect r);
  [DllImport("user32.dll", CharSet=CharSet.Unicode)] static extern IntPtr SendMessage(IntPtr h, uint msg, IntPtr wp, string text);
  [DllImport("user32.dll", CharSet=CharSet.Unicode)] static extern IntPtr SendMessage(IntPtr h, uint msg, IntPtr wp, StringBuilder text);
  [DllImport("user32.dll", CharSet=CharSet.Unicode)] static extern IntPtr SendMessageTimeout(IntPtr h,uint m,IntPtr w,StringBuilder b,uint flags,uint ms,out IntPtr result);
  [DllImport("user32.dll")] static extern bool PostMessage(IntPtr h, uint msg, IntPtr wp, IntPtr lp);
  [DllImport("user32.dll")] static extern IntPtr GetParent(IntPtr h);
  [DllImport("user32.dll")] static extern bool PrintWindow(IntPtr h,IntPtr dc,uint flags);
  [DllImport("user32.dll")] static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] static extern void keybd_event(byte key,byte scan,uint flags,UIntPtr extra);
  [DllImport("user32.dll")] static extern IntPtr SendMessage(IntPtr h,uint m,IntPtr w,IntPtr l);
  [DllImport("kernel32.dll")] static extern IntPtr OpenProcess(uint a,bool inherit,uint pid);
  [DllImport("kernel32.dll")] static extern IntPtr VirtualAllocEx(IntPtr p,IntPtr a,uint n,uint t,uint protection);
  [DllImport("kernel32.dll")] static extern bool VirtualFreeEx(IntPtr p,IntPtr a,uint n,uint t);
  [DllImport("kernel32.dll")] static extern bool WriteProcessMemory(IntPtr p,IntPtr a,byte[] b,int n,out IntPtr done);
  [DllImport("kernel32.dll")] static extern bool ReadProcessMemory(IntPtr p,IntPtr a,byte[] b,int n,out IntPtr done);
  [DllImport("kernel32.dll")] static extern bool CloseHandle(IntPtr p);
  struct Rect { public int left, top, right, bottom; }
  static bool Allowed(IntPtr h) {
    uint pid; GetWindowThreadProcessId(h,out pid);
    try {string name=Process.GetProcessById((int)pid).ProcessName.ToLower();return name=="mastro"||name=="winecontrols"||name=="operator"||name=="operatorsafe";} catch {return false;}
  }
  static string Txt(IntPtr h) {StringBuilder b=new StringBuilder(4096);IntPtr result;if(SendMessageTimeout(h,0xD,new IntPtr(b.Capacity),b,2,100,out result)==IntPtr.Zero)GetWindowText(h,b,b.Capacity);return b.ToString().Replace("\r"," ").Replace("\n"," ");}
  static bool Show(IntPtr h,IntPtr p) {
    if(!Allowed(h)||!IsWindowVisible(h)) return true;
    Rect r;GetWindowRect(h,out r);StringBuilder c=new StringBuilder(256);GetClassName(h,c,c.Capacity);
    Console.WriteLine("{0:X} parent={1:X} enabled={2} ({3},{4},{5},{6}) {7} | {8}",h.ToInt64(),GetParent(h).ToInt64(),IsWindowEnabled(h),r.left,r.top,r.right-r.left,r.bottom-r.top,c,Txt(h));
    return true;
  }
  [STAThread]
  static void Main(string[] args) {
    try {Run(args);} catch(Exception e) {Console.Error.WriteLine(e.ToString());Environment.ExitCode=1;}
  }
  static void Run(string[] args) {
    if(args.Length==0||args[0]=="list") {
      if(args.Length>1){IntPtr root=new IntPtr(Convert.ToInt64(args[1],16));if(!Allowed(root))throw new Exception("Target is not Mastro");Show(root,IntPtr.Zero);EnumChildWindows(root,Show,IntPtr.Zero);}
      else EnumWindows(delegate(IntPtr h,IntPtr p){if(Allowed(h)){Show(h,p);if(Txt(h).IndexOf("Mastro Expert")<0)EnumChildWindows(h,Show,p);}return true;},IntPtr.Zero);
      return;
    }
    IntPtr target=new IntPtr(Convert.ToInt64(args[1],16));if(!Allowed(target))throw new Exception("Target is not Mastro");
    if(args[0]=="clipboard") Console.Write(System.Windows.Forms.Clipboard.GetText());
    else if(args[0]=="items") {
      // Standard ListView UI-message buffers, not application database access.
      uint pid;GetWindowThreadProcessId(target,out pid);IntPtr process=OpenProcess(0x38,false,pid);
      IntPtr mem=VirtualAllocEx(process,IntPtr.Zero,8192,0x3000,4);if(mem==IntPtr.Zero)throw new Exception("Cannot allocate ListView message buffer");
      try {
        int n=SendMessage(target,0x1004,IntPtr.Zero,IntPtr.Zero).ToInt32();
        IntPtr header=SendMessage(target,0x101F,IntPtr.Zero,IntPtr.Zero);int columns=header==IntPtr.Zero?7:SendMessage(header,0x1200,IntPtr.Zero,IntPtr.Zero).ToInt32();
        Console.WriteLine("rows="+n+" columns="+columns);
        for(int row=0;row<Math.Min(n,40);row++) {
          string line="";
          for(int col=0;col<Math.Min(columns,64);col++) {
            byte[] item=new byte[64];Array.Copy(BitConverter.GetBytes(col),0,item,8,4);Array.Copy(BitConverter.GetBytes(mem.ToInt32()+128),0,item,20,4);Array.Copy(BitConverter.GetBytes(1024),0,item,24,4);
            IntPtr done;WriteProcessMemory(process,mem,item,item.Length,out done);SendMessage(target,0x1073,new IntPtr(row),mem);
            byte[] text=new byte[2048];ReadProcessMemory(process,new IntPtr(mem.ToInt32()+128),text,text.Length,out done);line+=" | "+Encoding.Unicode.GetString(text).Split('\0')[0];
          }
          Console.WriteLine(row+line);
        }
      } finally {VirtualFreeEx(process,mem,0,0x8000);CloseHandle(process);}
    }
    else if(args[0]=="capture") {
      Rect r;GetWindowRect(target,out r);
      using(Bitmap b=new Bitmap(r.right-r.left,r.bottom-r.top)) {
        using(Graphics g=Graphics.FromImage(b)){IntPtr dc=g.GetHdc();try{if(!PrintWindow(target,dc,0))throw new Exception("Capture failed");}finally{g.ReleaseHdc(dc);}}
        b.Save(args[2],ImageFormat.Png);
      }
    }
    else if(args[0]=="mouse") {
      int x=Convert.ToInt32(args[2]),y=Convert.ToInt32(args[3]);IntPtr point=new IntPtr(x|(y<<16));
      PostMessage(target,0x201,new IntPtr(1),point);PostMessage(target,0x202,IntPtr.Zero,point);
    }
    else if(args[0]=="shortcut") {
      if(!SetForegroundWindow(target))throw new Exception("Cannot focus verified Mastro window");
      System.Threading.Thread.Sleep(100);
      byte[] keys=new byte[args.Length-2];for(int i=2;i<args.Length;i++)keys[i-2]=Convert.ToByte(args[i],16);
      try {foreach(byte key in keys)keybd_event(key,0,0,UIntPtr.Zero);}
      finally {for(int i=keys.Length-1;i>=0;i--)keybd_event(keys[i],0,2,UIntPtr.Zero);}
    }
    else if(args[0]=="close") PostMessage(target,0x10,IntPtr.Zero,IntPtr.Zero);
    else if(args[0]=="click") PostMessage(target,0xF5,IntPtr.Zero,IntPtr.Zero);
    else if(args[0]=="set") SendMessage(target,0xC,IntPtr.Zero,args[2]);
    else if(args[0]=="key") {int key=Convert.ToInt32(args[2],16);PostMessage(target,0x100,new IntPtr(key),IntPtr.Zero);PostMessage(target,0x101,new IntPtr(key),IntPtr.Zero);}
    else throw new Exception("Unknown operation");
  }
}
