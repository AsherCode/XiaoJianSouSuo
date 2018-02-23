/*
SQLyog Ultimate v8.53 
MySQL - 5.6.17 : Database - xjr
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
/*Table structure for table `cai` */

DROP TABLE IF EXISTS `cai`;

CREATE TABLE `cai` (
  `consume` varchar(255) DEFAULT NULL,
  `post_url` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `popularity` varchar(255) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `author` varchar(255) DEFAULT NULL,
  `advantage` varchar(255) DEFAULT NULL,
  `url_object_id` varchar(11) NOT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`url_object_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `job` */

DROP TABLE IF EXISTS `job`;

CREATE TABLE `job` (
  `url` varchar(300) NOT NULL,
  `url_object_id` varchar(50) NOT NULL,
  `title` varchar(100) NOT NULL,
  `salary` varchar(20) DEFAULT NULL,
  `job_city` varchar(10) DEFAULT NULL,
  `work_years` varchar(100) DEFAULT NULL,
  `degree_need` varchar(30) DEFAULT NULL,
  `job_type` varchar(20) DEFAULT NULL,
  `publish_time` varchar(20) NOT NULL,
  `tags` varchar(100) DEFAULT NULL,
  `job_advantage` longtext,
  `job_desc` longtext NOT NULL,
  `job_addr` varchar(50) DEFAULT NULL,
  `company_url` varchar(300) DEFAULT NULL,
  `company_name` varchar(100) DEFAULT NULL,
  `crawl_time` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `crawl_update_time` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`url_object_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `jobbole_article` */

DROP TABLE IF EXISTS `jobbole_article`;

CREATE TABLE `jobbole_article` (
  `title` varchar(200) NOT NULL,
  `create_date` date DEFAULT NULL,
  `url` varchar(300) NOT NULL,
  `url_object_id` varchar(50) NOT NULL DEFAULT '',
  `front_image_url` varchar(300) NOT NULL,
  `front_image_path` varchar(200) DEFAULT NULL,
  `comment_nums` int(11) DEFAULT '0',
  `fav_nums` int(11) DEFAULT '0',
  `praise_nums` int(11) DEFAULT '0',
  `tags` varchar(200) DEFAULT NULL,
  `content` longtext NOT NULL,
  PRIMARY KEY (`url_object_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `movies` */

DROP TABLE IF EXISTS `movies`;

CREATE TABLE `movies` (
  `url_object_id` varchar(100) NOT NULL,
  `url` varchar(300) DEFAULT NULL,
  `description` longtext,
  `title` varchar(255) DEFAULT NULL,
  `create_date` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `front_image_url` varchar(255) DEFAULT NULL,
  `tags` varchar(255) DEFAULT NULL,
  `score` varchar(10) DEFAULT NULL,
  `duration` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`url_object_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `zhihu_answer` */

DROP TABLE IF EXISTS `zhihu_answer`;

CREATE TABLE `zhihu_answer` (
  `zhihu_id` varchar(50) NOT NULL,
  `url` varchar(300) NOT NULL,
  `title` varchar(300) DEFAULT NULL,
  `question_id` bigint(20) NOT NULL,
  `author_id` varchar(100) DEFAULT NULL,
  `content` longtext NOT NULL,
  `parise_num` int(11) NOT NULL DEFAULT '0',
  `comments_num` int(11) NOT NULL DEFAULT '0',
  `create_time` date NOT NULL,
  `update_time` date NOT NULL,
  `crawl_time` datetime NOT NULL ON UPDATE CURRENT_TIMESTAMP,
  `crawl_update_time` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `author_name` varchar(50) DEFAULT NULL,
  `answer_num` int(10) DEFAULT NULL,
  PRIMARY KEY (`zhihu_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `zhihu_question` */

DROP TABLE IF EXISTS `zhihu_question`;

CREATE TABLE `zhihu_question` (
  `zhihu_id` varchar(50) NOT NULL,
  `topics` varchar(255) DEFAULT NULL,
  `url` varchar(300) NOT NULL,
  `title` varchar(200) NOT NULL,
  `content` longtext NOT NULL,
  `create_time` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `update_time` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `answer_num` int(11) NOT NULL DEFAULT '0',
  `comments_num` int(11) NOT NULL DEFAULT '0',
  `watch_user_num` int(11) NOT NULL DEFAULT '0',
  `click_num` int(11) NOT NULL DEFAULT '0',
  `crawl_time` datetime NOT NULL ON UPDATE CURRENT_TIMESTAMP,
  `crawl_update_time` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`zhihu_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
