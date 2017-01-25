package tool
{
	import flash.events.TimerEvent;
	import flash.utils.Timer;

	/**
	 * 和服务器进行数据交互的封装类
	 * @author:js
	 * @E-mail:pfjhetg@qq.com
	 * 2013-12-29 下午10:11:54
	 */
	public class Message
	{
		/**登陆*/
		public static const LOGIN:uint = 1;
		/**心跳接口*/
		public static const TIMER:uint = 2;
		/**其他如抢地主，强退等指令*/
		public static const HANDLE:uint = 3;
		/**请求发牌*/
		public static const DEAL:uint = 4;
		/**心跳*/
		private var timer:Timer = new Timer(10000);
		
		private static var _instance:Message;
		
		/**cookie数组*/
		public var list:Array = [];
		
		public static function getInstance():Message
		{
			if(!_instance)
				_instance = new Message(new Inner());
			return _instance;
		}
		
		public function Message(inner:Inner)
		{
			timer.addEventListener(TimerEvent.TIMER, onTimer);
			timer.start();
			list = [];
			list.push("[1,[6326, 'ddd33', '0B1026A8FA261407426E6CC90D2F0845']]"); //添加3个用户
			list.push("[1,[6437, 'ddd44', 'FF7467D5C324BB3AE0B2C69309808265']]");
			list.push("[1,[6443, 'ddd55', '64D8F55F5A4CDC75C707A0D7C579BFAC']]");
		}
		
		/**登陆*/
		public function login():void
		{
			var msg:String = list.shift(); //取出一条测试数据
			MySocket.getInstance().sendMessage(LOGIN, msg);
		}

		/**发牌*/
		public function deal():void
		{
			var msg:String = "[4,[]]";
			MySocket.getInstance().sendMessage(DEAL, msg);
		}
		
		/**心跳10秒一次*/
		private function heartBeat():void
		{
			var msg:String = "[2]";
			MySocket.getInstance().sendMessage(TIMER, msg);
		}
		
		/**请求游戏队列*/
		public function gameQueue():void
		{
			var msg:String = "[2,[5,1]]";
			MySocket.getInstance().sendMessage(HANDLE, msg);
		}
		
		/**开始心跳*/
		public function timerStart():void
		{
			timer.start();
		}
		
		/**暂停心跳*/
		public function timerStop():void
		{
			timer.stop();
		}
		
		private function onTimer(e:TimerEvent):void
		{
			heartBeat();
		}
		
		/**抢地主（1分，2分，3分）*/
		public function LootLandowner(point:int):void
		{
			var msg:String = "[2,[1,"+ point +"]]";
			MySocket.getInstance().sendMessage(HANDLE, msg);
		}
		
		/**不抢*/
		public function noLoot():void
		{
			var msg:String = "[2,[2]]";
			MySocket.getInstance().sendMessage(HANDLE, msg);
		}
		
		/**出牌*/
		public function chupai(str:String = ''):void
		{
			var msg:String = "[2,[3, "+ str +"]]";
			MySocket.getInstance().sendMessage(HANDLE, msg);
		}
		
		/**不出*/
		public function pass():void
		{
			var msg:String = "[2,[4]]";
			MySocket.getInstance().sendMessage(HANDLE, msg);
		}
	}
}

class Inner
{
	
}
