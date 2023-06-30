--User Table : 장고 migrate로 재생성 가능성 있음

CREATE TABLE `sMartpaLm`.`user` (
  'user_id' INT NOT NULL,
  `email` VARCHAR(200) NOT NULL,
  `user_name` VARCHAR(100) NULL,
  `password` VARCHAR(45) NULL,
  `is_active` CHAR(1) NULL,
  `is_step` CHAR(1) NULL,
  `nick_name` VARCHAR(45) NULL,
  PRIMARY KEY (`user_id`));


--농장
CREATE TABLE `sMartpaLm`.`farm` (
  `farm_id` VARCHAR(10) NOT NULL,
  `user_id` INT NOT NULL,
  `location` VARCHAR(500) NULL,
  `start_date` DATE NULL,
  `autocontrol_yn` CHAR(1) NULL DEFAULT 'N',
  `use_yn` CHAR(1) NULL DEFAULT 'Y',
  `crop_id` INT NULL,
  PRIMARY KEY (`farm_id`, `user_id`));

--작물
CREATE TABLE `sMartpaLm`.`crop` (
  `crop_id` INT NOT NULL,
  `crop_name` VARCHAR(100) NOT NULL,
  `crop_temperature` FLOAT NULL,
  `crop_humidity` FLOAT NULL,
  `crop_nutrition` VARCHAR(500) NULL,
  `crop_description` VARCHAR(500) NULL,
  PRIMARY KEY (`crop_id`));

--병충해
CREATE TABLE `sMartpaLm`.`disease` (
  `crop_id` INT NOT NULL,
  `disease_id` INT NOT NULL,
  `disease_nm` VARCHAR(100) NULL,
  `disease_img` VARCHAR(200) NULL,
  `disease_symptom` VARCHAR(200) NULL,
  `disease_action` VARCHAR(500) NULL,
  PRIMARY KEY (`crop_id`, `disease_id`));


--센서 데이터
CREATE TABLE `sMartpaLm`.`sensored_data` (
  `user_id` INT NOT NULL,
  `farm_id` VARCHAR(45) NOT NULL,
  `sensor_date_num` VARCHAR(45) NOT NULL,
  `co2_density` FLOAT NULL,
  `light_amount` FLOAT NULL,
  `temperature` FLOAT NULL,
  `humidity` FLOAT NULL,
  `nutrition_amt` FLOAT NULL,
  'status_img' VARCHAR(200) NULL,
  `predicted_status` VARCHAR(500) NULL,
  PRIMARY KEY (`user_id`, `farm_id`, `sensor_date_num`));

--병충해별 조치
CREATE TABLE `sMartpaLm`.`cure` (
  `crop_id` INT NOT NULL,
  `disease_id` INT NOT NULL,
  `syptom` VARCHAR(500) NULL,
  `action` VARCHAR(500) NULL,
  PRIMARY KEY (`crop_id`, `disease_id`));


