package tool
{
	import com.adobe.serialization.json.JSON;
	
	import flash.events.Event;
	import flash.events.ProgressEvent;
	import flash.net.Socket;
	import flash.utils.ByteArray;
	
	import audio.SoundEngine;
	
	import game.GameEndView;
	import game.GameView;
	import game.HallView;

	/**
	 * 套接字
	 * @author:js
	 * @E-mail:pfjhetg@qq.com
	 * 2013-12-29 下午9:23:28
	 */
	public class MySocket
	{
		private static const HEAD_0:int = 127;
		private static const HEAD_1:int = 12;
		private static const HEAD_2:int = 24;
		private static const HEAD_3:int = 22;
		private static const PROTO_VER:int = 65;
		private static const SERVER_VER:uint = 1;
		private static const HEAD_LENGHT:int = 4;
		private static const HEAD_CHUNK_LENGTH:int = 17;
		/**每一条消息数据长度*/
		private var dataLength:int = 0;
		/**套接字*/
		private var _socket:Socket;
		/**是否读取过协议头*/
		private var isReadHead:Boolean = false;
		
		private static var _mySocket:MySocket;
		
		public static function getInstance():MySocket
		{
			if(!_mySocket)
				_mySocket = new MySocket(new Inner());
			return _mySocket;
		}
		
		public function MySocket(inner:Inner)
		{
			_socket = new Socket();
			_socket.addEventListener(Event.CONNECT, onConnect);
			_socket.addEventListener(ProgressEvent.SOCKET_DATA, socketData);
		}
		
		/**获得套接字*/
		public function get socket():Socket
		{
			return _socket;
		}

		public function connect():void
		{
			_socket.connect("127.0.0.1", 10000);
		}
		
		protected function onConnect(event:Event):void
		{
			trace('连接');
			Message.getInstance().login();
		}
		
		/**获取服务器返回信息*/
		protected function socketData(event:Event):void
		{
			//处理粘包
			while(true)
			{
				if(_socket.bytesAvailable >= HEAD_CHUNK_LENGTH)
				{
					var head:ByteArray = new ByteArray();
					_socket.readBytes(head, 0, HEAD_CHUNK_LENGTH);
					//这里按照加密的顺序来解密
					dataLength = head.readByte();
					dataLength = head.readByte();
					dataLength = head.readByte();
					dataLength = head.readByte();
					
					dataLength = head.readByte();
					
					dataLength = head.readInt();
					dataLength = head.readInt() - 4;
					var temp:ByteArray = new ByteArray();
					_socket.readBytes(temp, 0, dataLength);
					var s:String = temp.readUTFBytes(temp.bytesAvailable);
					var list:Array = s.split('(end)');//去掉每个消息最后的一个标识得到新的消息组成的数组
					var o:Object = com.adobe.serialization.json.JSON.decode(list.shift());
					readData(o);
				}
				else
				{
					break;
				}
			}
		}
		
		/**读取消息*/
		protected function readData(o:Object):void
		{
			//登陆
			if(o.s == 1)//取值成功
			{
				if(o.m == "验证成功" && o.c == null)
				{
					//ExternalInterface//取出进度条gif
//					ExternalInterface.call("flash_ok");
					GameStage.getInstance().firstLayer.addChild(HallView.getInstance());
					//大厅
					GameStage.getInstance().firstLayer.addChild(HallView.getInstance().res);
				}
				//操作
				if(o.c)
				{
					trace(o.c);
					var arr:Array;
					if(o.m)
						trace(o.m);
					switch(o.c)
					{
						case 1000://向玩家发牌
							//舞台加游戏桌面
							GameView.getInstance().initialize(o.f_p, o.s_p, o.t_p, o.d);
							if(GameStage.getInstance().firstLayer.contains(HallView.getInstance().res))
								GameStage.getInstance().firstLayer.removeChild(HallView.getInstance().res);
							if(!GameStage.getInstance().firstLayer.contains(GameView.getInstance().res))
								GameStage.getInstance().firstLayer.addChild(GameView.getInstance().res);
							break;
						case 1001:
							trace("你已经加入队列");
							break;
						case 1002://退出队列
							break;
						case 2000://更新PID和重置倒计时
							if(!o.p)
							{
								trace("没人抢地主，请等待重新发牌");
							}
							else
							{
								if(o.n_u)//当前操作用户，例如弃权的用户(如果没得，就是首次进入游戏系统自主选地主)
								{
									GameView.getInstance().clock.start(o.p, 30);//倒计时
									GameView.getInstance().updateHandle(o.p, 1, o.f);
								}
								else//如果没得，就是首次进入游戏系统自主选地主
								{	
									GameView.getInstance().clock.start(o.p, 30);//倒计时
									GameView.getInstance().updateHandle(o.p, 1, o.f);
								}
							}
							break;
						case 2001://重新发牌
							GameView.getInstance().resetPoker(o.f_p, o.s_p, o.t_p, o.d);
							break;
						case 2002://是抢地主完成，并获取地主用户的牌数d_z地主牌，dz_u:地主。
							GameView.getInstance().poker.onShow(o.d_z);
							if(GameView.getInstance().user.postion != o.dz_u)//排除地主是自己。是自己执行2003里面的方法
							{
								if(GameView.getInstance().enemy_1.postion == o.dz_u)
								{
									GameView.getInstance().enemy_1.pokerContainer.addPoker(3);
									GameView.getInstance().RoleShow();
									GameView.getInstance().roleList[0].gotoAndStop(1);
									GameView.getInstance().roleList[1].gotoAndStop(2);
									GameView.getInstance().roleList[2].gotoAndStop(2);
								}
								else
								{
									GameView.getInstance().enemy_2.pokerContainer.addPoker(3);
									GameView.getInstance().RoleShow();
									GameView.getInstance().roleList[0].gotoAndStop(2);
									GameView.getInstance().roleList[1].gotoAndStop(1);
									GameView.getInstance().roleList[2].gotoAndStop(2);
								}
							}
							//游戏开始
							GameView.getInstance().clock.start(o.dz_u, 30);
							break;
						case 2003://更新当前地主用户的牌组（获取地主牌后的牌组，只要自己是地主时候才收到此消息）
							GameView.getInstance().user.initialize(o.p, null);
							//更新角色图标
							GameView.getInstance().RoleShow();
							GameView.getInstance().roleList[0].gotoAndStop(2);
							GameView.getInstance().roleList[1].gotoAndStop(2);
							GameView.getInstance().roleList[2].gotoAndStop(1);
							GameView.getInstance().clock.start(GameView.getInstance().user.postion, 30);
							GameView.getInstance().updateHandle(GameView.getInstance().user.postion, 2);
							break;
						case 2004://不抢地主(非系统时间到了弃权，是用户自主弃权)
							GameView.getInstance().updateHandle(o.n_u, 3, o.f);
							break;
						case 2010://报警
							trace(o.m);
							arr = o.mp3.split(".");
							SoundEngine.getInstance().playSound(arr[0]);
							switch(o.m)
							{
								case "还剩2张牌了":
									break;
								case "还剩1张牌了":
									break;
							}
							break;
						case 2011://推送数据，告诉客户端该下一个用户出牌了，如果p=''，则表示上家是不出，n=上家，next=该出牌的下家
							if(o.p)//更新牌
							{
								GameView.getInstance().updateChupai(o.n, o.p);
								GameView.getInstance().chupai(o.p);
								//播放mp3
								arr = o.mp3.split(".");
								SoundEngine.getInstance().playSound(arr[0]);
							}//计时器跳入下一个玩家
							GameView.getInstance().clock.start(o.next, 30);
							GameView.getInstance().updateHandle(o.next, 2);
							//播放mp3
							arr = o.mp3.split(".");
							SoundEngine.getInstance().playSound(arr[0]);
							break;
						case 2012://游戏结束了,w=胜利者list数组，l=失败者list数组，d=底价，losemoney=输的金额，winmoney=赢的money
							GameStage.getInstance().gameLayer.addChild(GameEndView.getInstance());
							
							break;
						case 2013://用户放弃了，p=放弃出牌的用户
							trace(o.p + "放弃出牌");
							break;
						case 2016://游戏结束，返回大厅
							trace("游戏结束");
							GameStage.getInstance().firstLayer.removeChild(GameView.getInstance().res);
							GameStage.getInstance().firstLayer.addChild(HallView.getInstance().res);
							break;
					}
				}
				else
				{
//					trace("心跳");
				}
			}
			
			
			if(o.s != 1)//失败,错误
			{
				if(o.c)//有指令
				{
					trace(o.c +"下一句不是一样的证明就是m");
					if(o.m)
						trace(o.m);
					switch(o.c)
					{
						case 2005://抢地主失败，销毁计时器和按钮
							GameView.getInstance().user.handleContainer.updateShow(3);
							break;
						case 2006://抢地主失败，重新开启计数器按钮
							GameView.getInstance().user.handleContainer.updateShow(1);
							break;
						case 2007://用户不抢地主失败，销毁资源
							GameView.getInstance().user.handleContainer.updateShow(3);
							break;
						case 2008://用户出牌失败，销毁出牌资源
							GameView.getInstance().user.handleContainer.updateShow(3);
							break;
						case 2009://用户出牌失败，重新生成对应资源
							GameView.getInstance().user.handleContainer.updateShow(2);
							break;
						case 2014://不出失败，销毁出牌资源
							GameView.getInstance().user.handleContainer.updateShow(3);
							break;
						case 2015://不出失败，重新生成出牌交互
							GameView.getInstance().user.handleContainer.updateShow(5);
							break;
						case 2017://用户错误强行断开用户
							
							break;
					}
				}
				else
				{
					if(o.m == "您还未登录")
					{
						Message.getInstance().login();//重新登陆
						trace(o.m);
					}
				}
			}
		}
		
		/**
		 * 发送消息
		 * @param code 指令号
		 * @param msg 消息内容
		 * 
		 */		
		public function sendMessage(code:uint, msg:String):void
		{
			this.socket.writeBytes(pack(code, msg));
			this.socket.flush();
		}
		
		/**
		 * 用ByteArray封装协议 
		 * @param code 指令号
		 * @param msg 消息内容
		 * @return 
		 * 
		 */		
		private function pack(code:uint, msg:String):ByteArray
		{
			var bytes:ByteArray = new ByteArray();
			
			bytes.writeByte(HEAD_0);
			bytes.writeByte(HEAD_1);
			bytes.writeByte(HEAD_2);
			bytes.writeByte(HEAD_3);
			
			bytes.writeByte(PROTO_VER);
			bytes.writeUnsignedInt(SERVER_VER);
			
			bytes.writeUnsignedInt(msg.length + 4);
			bytes.writeUnsignedInt(code);//code是方法类型
			
			bytes.writeUTFBytes(msg); //msg是传递的字串信息
			
			bytes.position = 0;
			
			return bytes;
		}
	}
}

class Inner
{
	
}

