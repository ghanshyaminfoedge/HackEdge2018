create database keystroke_data;

CREATE TABLE `keystroke` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(52) NOT NULL,
  `key_combo` varchar(52) NOT NULL,
  `data_array` varchar(512) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=latin1;

