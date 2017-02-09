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

INSERT INTO `lo_gamelog` (`gamelog_id`, `gamer_list`, `winner`, `loser`, `multiple`, `upset`, `add_time`, `add_ymd`) VALUES
(1, '2,6326,3', '2,6326', '3', 6, 1, 1390406089, '2014-01-22'),
(2, '2,6326,3', '2,6326', '3', 6, 1, 1390406357, '2014-01-22'),
(3, '2,6326,3', '2,6326', '3', 6, 1, 1390406563, '2014-01-23'),
(4, '3,6326,2', '3,6326', '2', 6, 1, 1390406668, '2014-01-23'),
(5, '6326,6437,6443', '6326,6437', '6443', 6, 1, 1390407449, '2014-01-23'),
(6, '6326,6437,6443', '6326,6437', '6443', 6, 1, 1390408909, '2014-01-23'),
(7, '6326,6437,6443', '6326,6437', '6443', 6, 1, 1390409152, '2014-01-23'),
(8, '6437,6326,6443', '6437,6326', '6443', 6, 1, 1390409243, '2014-01-23'),
(9, '6437,6443,6326', '6437,6443', '6326', 6, 1, 1390409365, '2014-01-23'),
(10, '6443,6437,6326', '6443,6437', '6326', 6, 1, 1390409585, '2014-01-23'),
(11, '6437,6443,6326', '6437,6443', '6326', 6, 1, 1390409752, '2014-01-23'),
(12, '6326,6437,6443', '6326,6437', '6443', 6, 1, 1390410430, '2014-01-23'),
(13, '6326,6437,6443', '6326,6437', '6443', 6, 1, 1390412919, '2014-01-23'),
(14, '6326,6437,6443', '6326,6437', '6443', 6, 1, 1390413091, '2014-01-23'),
(15, '6326,6437,6443', '6326,6437', '6443', 6, 1, 1390413367, '2014-01-23'),
(16, '6326,6437,6443', '6326,6437', '6443', 6, 1, 1390413737, '2014-01-23'),
(17, '6437,6326,6443', '6437,6326', '6443', 6, 1, 1390413930, '2014-01-23'),
(18, '6326,6443,6437', '6326,6443', '6437', 6, 1, 1390414211, '2014-01-23'),
(19, '6443,6437,6326', '6443,6437', '6326', 6, 1, 1390414642, '2014-01-23'),
(20, '6437,6326,6443', '6437,6326', '6443', 6, 1, 1390414953, '2014-01-23'),
(21, '6326,6437,6443', '6326,6437', '6443', 6, 1, 1390485817, '2014-01-23'),
(22, '6437,6326,6443', '6437,6326', '6443', 6, 1, 1390486279, '2014-01-23'),
(23, '6437,6326,6443', '6437,6326', '6443', 6, 1, 1390486780, '2014-01-23'),
(24, '6326,6437,6443', '6326,6437', '6443', 6, 1, 1390487039, '2014-01-23'),
(25, '6326,6443,6437', '6326,6443', '6437', 6, 1, 1390487332, '2014-01-23'),
(26, '6443,6326,6437', '6443,6326', '6437', 6, 1, 1390487571, '2014-01-23'),
(27, '6437,6326,6443', '6437,6326', '6443', 6, 1, 1390487770, '2014-01-23'),
(28, '6326,6437,6443', '6326,6437', '6443', 6, 1, 1390487868, '2014-01-23'),
(29, '6326,6437,6443', '6326,6437', '6443', 6, 1, 1390488233, '2014-01-23'),
(30, '6326,6443,6437', '6326,6443', '6437', 6, 1, 1390488388, '2014-01-23'),
(31, '6443,6437,6326', '6443,6437', '6326', 6, 1, 1390488710, '2014-01-23'),
(32, '6443,6326,6437', '6443,6326', '6437', 6, 1, 1390488860, '2014-01-23'),
(33, '6326,6437,6443', '6326,6437', '6443', 6, 1, 1390489537, '2014-01-23'),
(34, '6443,6326,6437', '6443,6326', '6437', 6, 1, 1390492445, '2014-01-23'),
(35, '6443,6326,6437', '6443,6326', '6437', 6, 1, 1390493364, '2014-01-24'),
(36, '6443,6437,6326', '6443,6437', '6326', 6, 1, 1390493419, '2014-01-24'),
(37, '6437,6326,6443', '6437,6326', '6443', 6, 1, 1390494592, '2014-01-24'),
(38, '6326,6443,6437', '6326,6443', '6437', 6, 1, 1390494668, '2014-01-24'),
(39, '6437,6443,6326', '6437,6443', '6326', 6, 1, 1390494996, '2014-01-24'),
(40, '6443,6326,6437', '6443,6326', '6437', 6, 1, 1390495301, '2014-01-24'),
(41, '6443,6437,6326', '6443,6437', '6326', 6, 1, 1390495427, '2014-01-24'),
(42, '6326,6437,6443', '6326,6437', '6443', 6, 1, 1390495502, '2014-01-24'),
(43, '6326,6443,6437', '6326,6443', '6437', 6, 1, 1390495592, '2014-01-24'),
(44, '6437,6326,6443', '6437,6326', '6443', 4, 1, 1390496754, '2014-01-24'),
(45, '6326,6443,6437', '6326,6443', '6437', 6, 1, 1390497625, '2014-01-24'),
(46, '6443,6326,6437', '6443,6326', '6437', 6, 1, 1390498168, '2014-01-24'),
(47, '6326,6443,6437', '6326,6443', '6437', 6, 1, 1390498436, '2014-01-24'),
(48, '6443,6326,6437', '6443,6326', '6437', 6, 1, 1390498645, '2014-01-24'),
(49, '6437,6326,6443', '6437,6326', '6443', 6, 1, 1390498743, '2014-01-24'),
(50, '6443,6437,6326', '6443,6437', '6326', 6, 1, 1390500059, '2014-01-24'),
(51, '6437,6326,6443', '6437,6326', '6443', 6, 1, 1390585308, '2014-01-25'),
(52, '6437,6443,6326', '6437,6443', '6326', 24, 1, 1390585718, '2014-01-25'),
(53, '6326,6437,6443', '6326,6437', '6443', 6, 1, 1390585798, '2014-01-25'),
(54, '6443,6326,6437', '6443,6326', '6437', 6, 1, 1390586062, '2014-01-25'),
(55, '6437,6326,6443', '6437,6326', '6443', 6, 1, 1390586328, '2014-01-25'),
(56, '6326,6437,6443', '6326,6437', '6443', 6, 1, 1390586573, '2014-01-25'),
(57, '6326,6437,6443', '6326,6437', '6443', 6, 1, 1390587050, '2014-01-25'),
(58, '6443,6437,6326', '6443,6437', '6326', 12, 1, 1390588065, '2014-01-25'),
(59, '6443,6326,6437', '6443,6326', '6437', 12, 1, 1390739522, '2014-01-26'),
(60, '6437,6443,6326', '6437,6443', '6326', 6, 1, 1390739689, '2014-01-26'),
(61, '6437,6326,6443', '6437,6326', '6443', 12, 1, 1390740074, '2014-01-26'),
(62, '6437,6326,6443', '6437,6326', '6443', 6, 1, 1390743181, '2014-01-26'),
(63, '6437,6326,6443', '6437,6326', '6443', 6, 1, 1390743769, '2014-01-26'),
(64, '6437,6443,6326', '6437,6443', '6326', 12, 1, 1390745026, '2014-01-26'),
(65, '6443,6326,6437', '6443,6326', '6437', 6, 1, 1390745637, '2014-01-26'),
(66, '6437,6326,6443', '6437,6326', '6443', 6, 1, 1390746230, '2014-01-26'),
(67, '6326,6437,6443', '6326,6437', '6443', 6, 1, 1390747037, '2014-01-26'),
(68, '6437,6443,6326', '6437,6443', '6326', 6, 1, 1390747220, '2014-01-26'),
(69, '6326,6443,6326', '6326', '6443,6326', 6, 1, 1390747390, '2014-01-26'),
(70, '6326,6443,6437', '6326,6443', '6437', 6, 1, 1390749683, '2014-01-26'),
(71, '6326,6437,6443', '6326,6437', '6443', 6, 1, 1390749881, '2014-01-26'),
(72, '6326,6437,6443', '6326,6437', '6443', 6, 1, 1390750123, '2014-01-26'),
(73, '6326,6443,6437', '6326,6443', '6437', 6, 1, 1390750535, '2014-01-26'),
(74, '6437,6326,6443', '6437,6326', '6443', 6, 1, 1390750683, '2014-01-26'),
(75, '6326,6443,6437', '6326,6443', '6437', 6, 1, 1390750887, '2014-01-26'),
(76, '6443,6326,6437', '6443,6326', '6437', 6, 1, 1390751458, '2014-01-26'),
(77, '6326,6437,6443', '6326', '6437,6443', 6, 1, 1390751601, '2014-01-26'),
(78, '6437,6326,6443', '6437,6326', '6443', 6, 1, 1390751844, '2014-01-26'),
(79, '6443,6326,6437', '6443,6326', '6437', 6, 1, 1390752142, '2014-01-27'),
(80, '6437,6437,6443', '6437', '6437,6443', 6, 1, 1390752350, '2014-01-27'),
(81, '6443,6326,6437', '6443,6326', '6437', 6, 1, 1390752702, '2014-01-27'),
(82, '6437,6326,6443', '6437', '6326,6443', 6, 1, 1390752914, '2014-01-27'),
(83, '6326,6437,6443', '6326', '6437,6443', 12, 1, 1390753102, '2014-01-27'),
(84, '6326,6443,6326', '6326', '6443,6326', 6, 1, 1390753370, '2014-01-27'),
(85, '6326,6326,6443', '6326', '6326,6443', 6, 1, 1390753607, '2014-01-27'),
(86, '6326,6437,6326', '6326', '6437,6326', 6, 1, 1390753804, '2014-01-27'),
(87, '6326,6326,6437', '6326', '6326,6437', 6, 1, 1390754051, '2014-01-27'),
(88, '6326,6443,6326', '6326', '6443,6326', 6, 1, 1390754492, '2014-01-27'),
(89, '6326,6437,6443', '6326', '6437,6443', 6, 1, 1390754711, '2014-01-27'),
(90, '6326,6326,6437', '6326', '6326,6437', 12, 1, 1390754874, '2014-01-27'),
(91, '6443,6326,6437', '6443', '6326,6437', 6, 1, 1390754982, '2014-01-27'),
(92, '6443,6326,6437', '6443,6326', '6437', 6, 1, 1390755679, '2014-01-27'),
(93, '6326,2,3', '6326,2', '3', 6, 1, 1391058379, '2014-01-30'),
(94, '2,6326,3', '2,6326', '3', 6, 1, 1391059136, '2014-01-30'),
(95, '6326,2,6326,3', '6326,2,6326', '3', 6, 1, 1391059209, '2014-01-30'),
(96, '2,6326,3', '2,6326', '3', 6, 1, 1391059310, '2014-01-30'),
(97, '6326,3,3', '6326,3', '3', 6, 1, 1391060297, '2014-01-30'),
(98, '2,3,6326', '2,3', '6326', 6, 1, 1391060336, '2014-01-30'),
(99, '6326,2,3', '6326,2', '3', 6, 1, 1391060732, '2014-01-30'),
(100, '6326,2,3', '6326,2', '3', 6, 1, 1391060762, '2014-01-30'),
(101, '6326,2,3', '6326,2', '3', 6, 1, 1391060839, '2014-01-30'),
(102, '3,2,2', '3,2', '2', 6, 1, 1391060863, '2014-01-30'),
(103, '3,6326,2', '3,6326', '2', 6, 1, 1391060977, '2014-01-30'),
(104, '6326,2,3', '6326,2', '3', 6, 1, 1391061252, '2014-01-30'),
(105, '3,2,6326', '3,2', '6326', 6, 1, 1391061284, '2014-01-30'),
(106, '3,6326,2', '3,6326', '2', 6, 1, 1391061350, '2014-01-30'),
(107, '6326,2,3', '6326,2', '3', 6, 1, 1391061777, '2014-01-30'),
(108, '6326,3,2', '6326,3', '2', 6, 1, 1391061832, '2014-01-30'),
(109, '2,6326,3', '2,6326', '3', 6, 1, 1391061950, '2014-01-30'),
(110, '6326,2,3', '6326,2', '3', 1, 1, 1391062633, '2014-01-30'),
(111, '3,6326,2', '3,6326', '2', 1, 1, 1391062664, '2014-01-30'),
(112, '6326,2,3', '6326,2', '3', 1, 1, 1391062906, '2014-01-30'),
(113, '2,6326,3', '2,6326', '3', 1, 1, 1391063121, '2014-01-30');

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

INSERT INTO `lo_logincache` (`id`, `pid`, `user_id`, `user_name`) VALUES
(1621, 0, 2, 'ddd44'),
(1622, 1, 6326, 'ddd33')

;

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

INSERT INTO `lo_rfloat` (`rfloat_id`, `user_id`, `r_status`, `action_type`, `money`, `after_money`, `add_time`, `add_ymd`, `note`) VALUES
(220, 2, 1, 4, 2, 12, 1391063121, '2014-01-30', '斗地主获胜获得奖金2元'),
(221, 6326, 1, 4, 2, 100766, 1391063121, '2014-01-30', '斗地主获胜获得奖金2元'),
(222, 3, 2, 3, 4, 148214, 1391063121, '2014-01-30', '斗地主逃跑输掉了4元奖金');

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

INSERT INTO `mn_heart` (`id`, `pid`, `heart_time`) VALUES
(1621, 0, 1391063924),
(1622, 1, 1391063924);

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

INSERT INTO `us_user` (`user_id`, `user_name`, `user_pass`, `pass_rand`, `balance`, `funds_key`, `is_lock`) VALUES
(52, 'dddd34', '7B10EAC5790BAC98EFDEAD570627EB4B', '3FrCr#3o', 0, '37E17254CE2F60925B40CFEE8C87E997', 1);

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

INSERT INTO `us_userbase` (`user_id`, `nick_name`, `email`, `phone`, `qq`, `q_one`, `a_one`, `q_two`, `a_two`, `credentials`, `credentials_img`, `add_time`, `add_ymd`, `add_ip`, `last_time`, `last_ymd`, `last_ip`) VALUES
(50, '', '', '', '', '', '', '', '', '', '', 1386689945, '2013-12-10', '', NULL, NULL, NULL),
(51, '', '', '', '', '', '', '', '', '', '', 1386689964, '2013-12-10', '', NULL, NULL, NULL),
(52, '', '', '', '', '', '', '', '', '', '', 1386689973, '2013-12-10', '', NULL, NULL, NULL);
