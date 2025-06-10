Custom Keypass to 1Pass Importing program to retain nested-hierarchy structure that was present in Keypass.

I started a journey with taking responsibility in my department of a painfully manual process that had already exceeded two years from previous engineers of migrating our customer base from keypass. 
The 1Pass CSV importing tool is very standard and we did not want to bulk import all our customers in a one dump loaded vault. This would also lose the much needed nested-structure that Keypass directory had and need individual vaults to share separated access.

**What this application is designed for:**
	1. Create individual vaults per customer and add permissions.
	2. Break down the XML sub-groups from Keypass.
	3. Has 3 stages to transfer from XML > CSV > JSON and pipes json to OP CLI. 
	4. Adds the keypass directory trail within the name of the 1pass item so you understand what the item is in relation to.
 
This is a use-case design and chances are you'll have to amend according to your Keypass customer directory structure, but you may only need to adjust the XML reader stage for this and will not take you nearly as much time as creating it.

**Programs/Stages**
This has a few programs to phase data, the CSV output allows you to validate data before pushing it to OP.  You need to export from Keypass XML Version 2 - (HTML does not contain URLs or Notes)
	1. multisite-phase-xml-to-csv.py
	2. convert-csv-to-jsons.py
	3. powershell-op-import-single-customer.ps1 (powershell)
 
Keypass Structure Design -
see the group/subgroups per customer
Main > Type of Customer > Customer Name > Prod/pre-prod > Sites
 
 ![image](https://github.com/user-attachments/assets/4c2f3f84-1221-49af-82dd-c721dcb50ba9)
 
**How to use**
My setup is WSL and Powershell - this is due to restrictions of installing OP in WSL. but you can use the python scripts without WSL just ensure the file directory is correctly mentioned in the name of the file you're importing.
	1. **Export Keypass XML 2**
File > Export > Keepass XML (2.x)  
 ![image](https://github.com/user-attachments/assets/07cb603e-83cf-434c-bdf3-0d82eead3992)

	
2. Describe the xml name subgroup names within multisite-phase-xml-to-csv.py 
In this case the export name is example_export.xml - I want the generated csv to be called example_export.csv and the keypass root group is 'company keypass' and sub-group is 'self-hosted customers' (ensure only updating these group names in lowercase within this script)
![image](https://github.com/user-attachments/assets/b9ce8831-f740-4fc6-9dd8-e845535fb46b)


3. The XML Export and python script are within the same directory - again I'm using WSL but you may wish to figure with cmd if you don't have that. 
![image](https://github.com/user-attachments/assets/0f3425fe-a27f-45f3-82d7-5ec3801b0db2)


4. the CSV is generated - their will be no records within this CSV if the subgroup names are incorrect in multisite-phase-xml-to-csv.py
![image](https://github.com/user-attachments/assets/9b712cd3-1529-4e1f-b7b4-beea902e9e42)

Verify the data looks correct to what was exported:
![image](https://github.com/user-attachments/assets/a91fa0cb-f366-4a1a-871a-e854349d9616)

5. Edit convert-csv-to-jsons.py
Add the csv and json file directory you wish to generate 
 
Now there's an individual json file for each customer to be imported to OP
![image](https://github.com/user-attachments/assets/fe406c9b-6a9f-49f3-b160-e6d1999faa78)

You can adjust permissions to push to the customer vault via editing powershell-op-import-single-customer.ps1
Add appropiate Emails and Group Names 
![image](https://github.com/user-attachments/assets/61684688-c9ee-4dca-aa81-97b2ec85727e)









![image](https://github.com/user-attachments/assets/1a0be581-7267-4c6a-bade-02c2630a7804)
