package tool
{
	import flash.utils.Dictionary;

	/**
	 * 消息管理器
	 * @author:js
	 * @E-mail:pfjhetg@qq.com
	 * 2013-12-29 上午3:08:16
	 */
	public class NotificationManager
	{
		
		private static var _instance:NotificationManager;
		
		/**消息容器*/
		private var dic:Dictionary;
		
		public function NotificationManager(inner:Inner)
		{
		}
		
		public static function getInstance():NotificationManager
		{
			if(!_instance)
				_instance = new NotificationManager(new Inner());
			return _instance;
		}
		
		/**注册消息*/
		public function register():void
		{
			
		}
		
		/**注销消息*/
		public function unregister():void
		{
			
		}
		
	}
}

class Inner
{
	
}



