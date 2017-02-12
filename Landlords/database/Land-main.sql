-- phpMyAdmin SQL Dump
-- version 2.11.9.2
-- http://www.phpmyadmin.net
--
-- 主机: 127.0.0.1:3306
-- 生成日期: 2014 年 02 月 07 日 13:31
-- 服务器版本: 5.1.28
-- PHP 版本: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- 数据库: `land_log`
--
CREATE DATABASE `land_log` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `land_log`;

-- --------------------------------------------------------

--
-- 表的结构 `lo_gamelog`
--

CREATE TABLE IF NOT EXISTS `lo_gamelog` (
  `gamelog_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `gamer_list` varchar(35) NOT NULL COMMENT '游戏参与者ID集合',
  `winner` varchar(23) NOT NULL COMMENT '如果是2人以逗号分隔',
  `loser` varchar(23) NOT NULL COMMENT '如果是2人以逗号分隔',
  `multiple` int(11) unsigned NOT NULL COMMENT '倍数',
  `upset` int(11) unsigned NOT NULL COMMENT '底价',
  `add_time` int(11) NOT NULL COMMENT '游戏时间',
  `add_ymd` date NOT NULL COMMENT '游戏时间冗余',
  PRIMARY KEY (`gamelog_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=114 ;

--
-- 导出表中的数据 `lo_gamelog`
--

-- INSERT INTO `lo_gamelog` (`gamelog_id`, `gamer_list`, `winner`, `loser`, `multiple`, `upset`, `add_time`, `add_ymd`) VALUES
-- (1, '2,6326,3', '2,6326', '3', 6, 1, 1390406089, '2014-01-22');

-- --------------------------------------------------------

--
-- 表的结构 `lo_logincache`
--

CREATE TABLE IF NOT EXISTS `lo_logincache` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `pid` int(11) unsigned NOT NULL,
  `user_id` int(11) unsigned NOT NULL,
  `user_name` varchar(256) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=1624 ;

--
-- 导出表中的数据 `lo_logincache`
--

-- INSERT INTO `lo_logincache` (`id`, `pid`, `user_id`, `user_name`) VALUES
-- (1, 0, 2, 'ddddd44');

-- --------------------------------------------------------

--
-- 表的结构 `lo_rfloat`
--

CREATE TABLE IF NOT EXISTS `lo_rfloat` (
  `rfloat_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(11) unsigned NOT NULL,
  `r_status` tinyint(1) unsigned NOT NULL COMMENT '资金类型，1：增加，2：扣除',
  `action_type` tinyint(1) unsigned NOT NULL COMMENT '操作的类型，1，充值，2，取现，3，游戏lose时扣除，4，游戏win时增加，5，活动赠送，6，其他',
  `money` int(11) unsigned NOT NULL COMMENT '操作的金额',
  `after_money` int(11) unsigned NOT NULL COMMENT '操作前的金额',
  `add_time` int(11) unsigned NOT NULL COMMENT '操作时间',
  `add_ymd` date NOT NULL COMMENT '操作时间冗余',
  `note` varchar(256) DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`rfloat_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=223 ;

--
-- 导出表中的数据 `lo_rfloat`
--

-- INSERT INTO `lo_rfloat` (`rfloat_id`, `user_id`, `r_status`, `action_type`, `money`, `after_money`, `add_time`, `add_ymd`, `note`) VALUES
-- (220, 1, 1, 4, 2, 12, 1391063121, '2014-01-30', '斗地主获胜获得奖金2元');

-- --------------------------------------------------------

--
-- 表的结构 `lo_useraction`
--

CREATE TABLE IF NOT EXISTS `lo_useraction` (
  `useraction_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(11) unsigned NOT NULL,
  `action_obj` varchar(256) NOT NULL COMMENT '操作的对象，多表请用逗号分隔',
  `action_key` int(11) NOT NULL COMMENT '修改的主键，只填主表的主键',
  `note` varchar(256) NOT NULL COMMENT '备注',
  PRIMARY KEY (`useraction_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

--
-- 导出表中的数据 `lo_useraction`
--


-- --------------------------------------------------------

--
-- 表的结构 `lo_userlogin`
--

CREATE TABLE IF NOT EXISTS `lo_userlogin` (
  `userlogin_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(11) unsigned NOT NULL,
  `add_time` int(11) unsigned NOT NULL COMMENT '登陆时间',
  `add_ymd` date NOT NULL COMMENT '登陆时间冗余',
  `add_ip` varchar(15) NOT NULL COMMENT '登陆IP',
  `status` tinyint(1) unsigned NOT NULL COMMENT '登陆状态，1：成功，2：失败',
  `note` varchar(256) DEFAULT NULL COMMENT '状态备注',
  PRIMARY KEY (`userlogin_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

--
-- 导出表中的数据 `lo_userlogin`
--

--
-- 数据库: `land_main`
--
CREATE DATABASE `land_main` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `land_main`;

-- --------------------------------------------------------

--
-- 表的结构 `mn_gamequeue`
--

CREATE TABLE IF NOT EXISTS `mn_gamequeue` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `pid` int(11) unsigned NOT NULL,
  `room_type` int(11) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1505 ;

--
-- 导出表中的数据 `mn_gamequeue`
--


-- --------------------------------------------------------

--
-- 表的结构 `mn_heart`
--

CREATE TABLE IF NOT EXISTS `mn_heart` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `pid` int(11) unsigned NOT NULL,
  `heart_time` int(11) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1624 ;

--
-- 导出表中的数据 `mn_heart`
--

-- INSERT INTO `mn_heart` (`id`, `pid`, `heart_time`) VALUES
-- (2, 0, 1391063924);

-- --------------------------------------------------------

--
-- 表的结构 `mn_room`
--

CREATE TABLE IF NOT EXISTS `mn_room` (
  `room_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `f_u` int(11) unsigned NOT NULL COMMENT '第一用户PID',
  `s_u` int(11) unsigned NOT NULL COMMENT '第二用户PID',
  `t_u` int(11) unsigned NOT NULL COMMENT '第三用户PID',
  `f_p` varchar(256) COLLATE utf8_bin NOT NULL COMMENT '第一用户扑克',
  `s_p` varchar(256) COLLATE utf8_bin NOT NULL COMMENT '第二用户扑克',
  `t_p` varchar(256) COLLATE utf8_bin NOT NULL COMMENT '第三用户扑克',
  `d_z` varchar(64) COLLATE utf8_bin NOT NULL COMMENT '地主牌',
  `dizhu_pid` int(11) unsigned DEFAULT NULL COMMENT '抢地主的PID',
  `timer` int(11) unsigned NOT NULL COMMENT '响应倒计时',
  `timer_pid` int(11) unsigned NOT NULL COMMENT '响应倒计时PID',
  `dz_pid` int(11) unsigned DEFAULT NULL COMMENT '地主的PID',
  `multiple` int(11) unsigned NOT NULL DEFAULT '1' COMMENT '倍率',
  `puke_type` tinyint(2) NOT NULL DEFAULT '0' COMMENT '当前出牌类型,0无类型，1：单牌，2：对子，3顺子，4，飞机，5，三带一，6，3带二，7，炸弹，8，四代二',
  `max_puke` varchar(256) COLLATE utf8_bin DEFAULT NULL COMMENT '当前最大牌',
  `dz_user` varchar(42) CHARACTER SET utf8 DEFAULT NULL COMMENT '有抢地主权限的PID集合',
  `spend` tinyint(1) unsigned NOT NULL DEFAULT '1' COMMENT '当前阶段，1，房间创建,2，抢地主，3，出牌',
  `now_pid` int(11) unsigned DEFAULT NULL COMMENT '当前出牌的ID，为空或0时表示一轮结束或没有出牌',
  `money_type` tinyint(1) unsigned DEFAULT NULL COMMENT 'money类型',
  PRIMARY KEY (`room_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=473 ;

--
-- 导出表中的数据 `mn_room`
--


-- --------------------------------------------------------

--
-- 表的结构 `mn_sysmsg`
--

CREATE TABLE IF NOT EXISTS `mn_sysmsg` (
  `sysmsg_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `from_userid` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '来源，系统消息必须0',
  `to_userid` int(11) unsigned NOT NULL COMMENT '收信者ID',
  `msg_title` tinyint(1) unsigned NOT NULL COMMENT '消息类型，1，公告，2，系统提醒，3，警报',
  `title` varchar(256) NOT NULL COMMENT '标题',
  `content` text NOT NULL COMMENT '内容',
  `read_type` tinyint(1) unsigned NOT NULL DEFAULT '1' COMMENT '阅读状态,1,未读，2，已读，3，已删除',
  `add_ymd` date NOT NULL COMMENT '发送时间冗余',
  `read_ymd` date DEFAULT NULL COMMENT '阅读时间冗余',
  PRIMARY KEY (`sysmsg_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

--
-- 导出表中的数据 `mn_sysmsg`
--


-- --------------------------------------------------------

--
-- 表的结构 `mn_usermsg`
--

CREATE TABLE IF NOT EXISTS `mn_usermsg` (
  `usermsg_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `from_userid` int(11) unsigned NOT NULL COMMENT '发信者ID',
  `to_userid` int(11) unsigned NOT NULL COMMENT '收信者ID',
  `msg_title` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '消息类型，必须0',
  `title` varchar(256) NOT NULL COMMENT '标题',
  `content` text NOT NULL COMMENT '内容',
  `read_type` tinyint(1) unsigned NOT NULL DEFAULT '1' COMMENT '阅读状态,1,未读，2，已读，3，已删除',
  `add_ymd` date NOT NULL COMMENT '发送时间冗余',
  `read_ymd` date DEFAULT NULL COMMENT '阅读时间冗余',
  PRIMARY KEY (`usermsg_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

--
-- 导出表中的数据 `mn_usermsg`
--

--
-- 数据库: `land_user`
--
CREATE DATABASE `land_user` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `land_user`;

-- --------------------------------------------------------

--
-- 表的结构 `us_user`
--

CREATE TABLE IF NOT EXISTS `us_user` (
  `user_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user_name` varchar(32) NOT NULL COMMENT '用户账号',
  `user_pass` varchar(64) NOT NULL COMMENT '用户密码',
  `pass_rand` varchar(8) NOT NULL COMMENT '密码随机码',
  `balance` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '用户余额',
  `funds_key` varchar(64) NOT NULL COMMENT '用户资金key',
  `is_lock` tinyint(1) unsigned NOT NULL DEFAULT '1' COMMENT '是否锁定,1:否，2，是',
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=53 ;

--
-- 导出表中的数据 `us_user`
--

-- INSERT INTO `us_user` (`user_id`, `user_name`, `user_pass`, `pass_rand`, `balance`, `funds_key`, `is_lock`) VALUES
-- (1, 'dddd34', '7B10EAC5790BAC98EFDEAD570627EB4B', '3FrCr#3o', 0, '37E17254CE2F60925B40CFEE8C87E997', 1);

-- --------------------------------------------------------

--
-- 表的结构 `us_userbase`
--

CREATE TABLE IF NOT EXISTS `us_userbase` (
  `user_id` int(11) unsigned NOT NULL,
  `nick_name` varchar(64) DEFAULT NULL COMMENT '用户昵称',
  `email` varchar(256) DEFAULT NULL COMMENT '邮箱',
  `phone` varchar(16) DEFAULT NULL COMMENT '手机',
  `qq` varchar(16) DEFAULT NULL COMMENT 'QQ',
  `q_one` varchar(256) DEFAULT NULL COMMENT '密码提示问题1',
  `a_one` varchar(256) DEFAULT NULL COMMENT '回答1',
  `q_two` varchar(256) DEFAULT NULL COMMENT '密码提示问题2',
  `a_two` varchar(256) DEFAULT NULL COMMENT '回答2',
  `credentials` varchar(20) DEFAULT NULL COMMENT '证件号',
  `credentials_img` text COMMENT '证件图片冗余',
  `add_time` int(11) unsigned NOT NULL COMMENT '注册时间',
  `add_ymd` date NOT NULL COMMENT '注册时间冗余',
  `add_ip` varchar(15) NOT NULL COMMENT '注册IP',
  `last_time` int(11) unsigned DEFAULT NULL COMMENT '最近登录时间',
  `last_ymd` date DEFAULT NULL COMMENT '最近登录时间冗余',
  `last_ip` varchar(15) DEFAULT NULL COMMENT '最近登录IP',
  PRIMARY KEY (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- 导出表中的数据 `us_userbase`
--

-- INSERT INTO `us_userbase` (`user_id`, `nick_name`, `email`, `phone`, `qq`, `q_one`, `a_one`, `q_two`, `a_two`, `credentials`, `credentials_img`, `add_time`, `add_ymd`, `add_ip`, `last_time`, `last_ymd`, `last_ip`) VALUES
-- (1, '', '', '', '', '', '', '', '', '', '', 1386689945, '2013-12-10', '', NULL, NULL, NULL);
