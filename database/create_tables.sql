

CREATE TABLE `staff` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(16) COLLATE latin1_general_ci DEFAULT NULL,
  `name` varchar(64) COLLATE latin1_general_ci DEFAULT NULL,
  `given_name` varchar(64) COLLATE latin1_general_ci DEFAULT NULL,
  `last_name` varchar(64) COLLATE latin1_general_ci DEFAULT NULL,
  `phone` varchar(32) COLLATE latin1_general_ci DEFAULT NULL,
  `extension` varchar(12) COLLATE latin1_general_ci DEFAULT NULL,
  `title` varchar(64) COLLATE latin1_general_ci DEFAULT NULL,
  `department` varchar(64) COLLATE latin1_general_ci DEFAULT NULL,
  `manager_user_id` varchar(64) COLLATE latin1_general_ci DEFAULT NULL,
  `city` varchar(64) COLLATE latin1_general_ci DEFAULT NULL,
  `branch` varchar(64) COLLATE latin1_general_ci DEFAULT NULL,
  `office` varchar(64) COLLATE latin1_general_ci DEFAULT NULL,
  `state` varchar(8) COLLATE latin1_general_ci DEFAULT NULL,
  `mailing_address` varchar(256) COLLATE latin1_general_ci DEFAULT NULL,
  `company` varchar(64) COLLATE latin1_general_ci DEFAULT NULL,
  `email` varchar(64) COLLATE latin1_general_ci DEFAULT NULL,
  `create_date` varchar(16) COLLATE latin1_general_ci DEFAULT NULL,
  `active` tinyint(4) NOT NULL DEFAULT 1,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=26259 DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;


CREATE TABLE `staff_email` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fkStaff` int(11) NOT NULL DEFAULT 0,
  `email` varchar(120) COLLATE latin1_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=MyISAM AUTO_INCREMENT=55278 DEFAULT CHARSET=latin1 COLLATE=latin1_general_ci;
