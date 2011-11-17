UserID update run:
1. Program run with 3 params: email, userID, password
2. Connect to pc with domain name extracted from userID
3. Update user info file in pc with domain name:
    3.1. If user is not stored then creates a new one and add to info file
    3.2. If user is existed then update
    
Ex:
mod_user.py myemail@yahoo.com ABCD1234@domain1.com mypassword
thì nó sẽ thay đổi file info trên server domain1.com
nếu chưa có user thì chèn vào fiel info 1 dòng:
ABCD1234@domain1.com:myemail@yahoo.com:mypassword
nếu UserID đã tồn tại trên máy đó rồi, thì update email AND/OR password
