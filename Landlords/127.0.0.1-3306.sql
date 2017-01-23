-- phpMyAdmin SQL Dump
-- version 2.11.9.2
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1:3306
-- Generation Time: Dec 22, 2013 at 04:10 PM
-- Server version: 5.1.28
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `land_main`
--
CREATE DATABASE `land_main` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `land_main`;

-- --------------------------------------------------------

--
-- Table structure for table `mn_room`
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
  `dizhu_pid` int(11) unsigned DEFAULT NULL COMMENT '地主PID',
  `timer` int(11) unsigned NOT NULL COMMENT '响应倒计时',
  `timer_pid` int(11) unsigned NOT NULL COMMENT '响应倒计时PID',
  `multiple` int(11) unsigned NOT NULL DEFAULT '1' COMMENT '倍率',
  `puke_type` tinyint(2) NOT NULL DEFAULT '0' COMMENT '当前出牌类型,0无类型，1：单牌，2：对子，3顺子，4，飞机，5，三带一，6，3带二，7，炸弹，8，四代二',
  `max_puke` varchar(10) COLLATE utf8_bin DEFAULT NULL COMMENT '当前最大牌',
  `spend` tinyint(1) unsigned NOT NULL DEFAULT '1' COMMENT '当前阶段，1，抢地主，2，出牌',
  PRIMARY KEY (`room_id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=2 ;

--
-- Dumping data for table `mn_room`
--

INSERT INTO `mn_room` (`room_id`, `f_u`, `s_u`, `t_u`, `f_p`, `s_p`, `t_p`, `d_z`, `dizhu_pid`, `timer`, `timer_pid`, `multiple`, `puke_type`, `max_puke`, `spend`) VALUES
(1, 1, 3, 4, 'bA,h4,hK,sJ,b7,fK,P1,f3,f4,f2,s8,hJ,b6,h5,f8,sK,h3', 'sQ,h6,bQ,h10,s7,fQ,h9,b4,b9,b3,s2,fJ,b8,hQ,f6,fA,s6', 'bK,b10,f9,f7,s4,h2,f5,bJ,b2,hA,s3,h7,s9,s10,P2,b5,s5', 'f10,h8,sA', NULL, 1387722220, 3, 1, 0, NULL, 1);

-- --------------------------------------------------------

--
-- Table structure for table `mn_sysmsg`
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
-- Dumping data for table `mn_sysmsg`
--


-- --------------------------------------------------------

--
-- Table structure for table `mn_usermsg`
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
-- Dumping data for table `mn_usermsg`
--

