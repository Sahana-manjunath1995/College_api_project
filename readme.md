### How to copy the Database Dump to the Destination Server?
docker cp student_data 952803436d01:/var/data/mysql


### How to restore the dump?
 mysql -uroot -proot College < student_data

### How to run docker mysql container with TCP ?
Expose port at 3306 with docker run command
mysql --host=localhost --protocol=TCP -uroot -proot