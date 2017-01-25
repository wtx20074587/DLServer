-- phpMyAdmin SQL Dump
-- version 2.11.9.2
-- http://www.phpmyadmin.net
--
-- 主机: 127.0.0.1:3306
-- 生成日期: 2014 年 02 月 07 日 13:33
-- 服务器版本: 5.1.28
-- PHP 版本: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- 数据库: `ssc_main`
--
CREATE DATABASE `ssc_main` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `ssc_main`;
-- --------------------------------------------------------

--
-- 表的结构 `mn_user`
--

CREATE TABLE IF NOT EXISTS `mn_user` (
  `user_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `user_name` varchar(16) NOT NULL COMMENT '用户名',
  `parent_id` int(11) unsigned DEFAULT NULL COMMENT '上级ID',
  `parent_name` varchar(16) DEFAULT NULL COMMENT '上级人名',
  `parent_root` text COMMENT '上级路径',
  `root_name` text COMMENT '上级名字',
  `user_pass` varchar(32) NOT NULL COMMENT '用户密码',
  `pass_key` varchar(8) NOT NULL COMMENT '密码随即码',
  `pay_pass` varchar(32) NOT NULL COMMENT '支付密码',
  `pay_key` varchar(8) NOT NULL COMMENT '支付随机码',
  `money` float(12,2) NOT NULL DEFAULT '0.00' COMMENT '余额',
  `qq` varchar(16) NOT NULL COMMENT 'qq',
  `add_time` int(11) unsigned NOT NULL COMMENT '注册时间',
  `add_ymd` date NOT NULL COMMENT '注册时间冗余',
  `add_ip` varchar(15) DEFAULT NULL COMMENT '注册IP',
  `last_time` int(11) DEFAULT NULL COMMENT '最后登录时间',
  `last_ymd` date DEFAULT NULL COMMENT '最后登录时间冗余',
  `last_ip` varchar(15) DEFAULT NULL COMMENT '最后登录IP',
  `is_lock` tinyint(1) unsigned NOT NULL DEFAULT '1' COMMENT '是否锁定1：，否，2，是',
  `is_daili` tinyint(1) unsigned NOT NULL DEFAULT '1' COMMENT '是否是代理：1不是，2是',
  `note` varchar(256) DEFAULT NULL COMMENT '锁定原因',
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

INSERT INTO `mn_user` (`user_id`, `user_name`, `user_pass`) VALUES
(3,'cccccc','123456'),
(4,'dddddd','123456'),
(5,'eeeeee','123456'),
(6,'ffffff','123456'),
(7,'aaaaaa','123456'),
(8,'bbbbbb','123456');