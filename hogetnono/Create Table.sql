-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema hogetnono
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema hogetnono
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `hogetnono` DEFAULT CHARACTER SET utf8 ;
USE `hogetnono` ;

-- -----------------------------------------------------
-- Table `hogetnono`.`APTinfo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `hogetnono`.`APTinfo` (
  `SN` VARCHAR(50) NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `address` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`SN`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hogetnono`.`transaction`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `hogetnono`.`transaction` (
  `code` INT NOT NULL AUTO_INCREMENT,
  `amount` INT NOT NULL,
  `date` DATETIME NOT NULL,
  `area` INT NOT NULL,
  `floor` INT NOT NULL,
  `APTinfo_SN` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`code`),
  INDEX `fk_transaction_APTinfo1_idx` (`APTinfo_SN` ASC) VISIBLE,
  CONSTRAINT `fk_transaction_APTinfo1`
    FOREIGN KEY (`APTinfo_SN`)
    REFERENCES `hogetnono`.`APTinfo` (`SN`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hogetnono`.`member`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `hogetnono`.`member` (
  `id` VARCHAR(30) NOT NULL,
  `pwd` VARCHAR(30) NOT NULL,
  `name` VARCHAR(25) NOT NULL,
  `tel` VARCHAR(25) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `hogetnono`.`board`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `hogetnono`.`board` (
  `code` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(45) NOT NULL,
  `date` DATETIME NOT NULL,
  `content` VARCHAR(100) NOT NULL,
  `member_id` VARCHAR(30) NOT NULL,
  `APTinfo_SN` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`code`),
  INDEX `fk_board_member_idx` (`member_id` ASC) VISIBLE,
  INDEX `fk_board_APT_info1_idx` (`APTinfo_SN` ASC) VISIBLE,
  CONSTRAINT `fk_board_member`
    FOREIGN KEY (`member_id`)
    REFERENCES `hogetnono`.`member` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_board_APT_info1`
    FOREIGN KEY (`APTinfo_SN`)
    REFERENCES `hogetnono`.`APTinfo` (`SN`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
