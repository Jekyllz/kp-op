**Custom Keypass to 1Pass Importing program to retain nested-hierarchy structure that was present in Keypass.**
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

My setup is WSL and Powershell - this is due to my works restriction of installing OP in WSL. 
but you can use the python scripts without WSL just ensure the file directory is correctly mentioned in the name of the file you're importing.

I assume you know how to use nano, linux, powershell in this guide. apologies if this is note the most detailed guide. 

**1. Export Keypass XML 2**
	File > Export > Keepass XML (2.x)  
	![image](https://github.com/user-attachments/assets/07cb603e-83cf-434c-bdf3-0d82eead3992)

**2. Describe the xml name subgroup names within multisite-phase-xml-to-csv.py **
	In this case the export name is example_export.xml -
	I want the generated csv to be called example_export.csv and the keypass root group is 'company keypass' and sub-group is 'self-hosted customers'
	(ensure only updating these group names in lowercase within this script)

	```nano multisite-phase-xml-to-csv.py```

	```python multisite-phase-xml-to-csv.py```

![image](https://github.com/user-attachments/assets/b9ce8831-f740-4fc6-9dd8-e845535fb46b)

**4. The XML Export and python script are within the same directory - again I'm using WSL but you may wish to figure with cmd if you don't have that. **
	![image](https://github.com/user-attachments/assets/0f3425fe-a27f-45f3-82d7-5ec3801b0db2)

**5. the CSV is generated - there will be no records within this CSV if the subgroup names are incorrect in multisite-phase-xml-to-csv.py**
	![image](https://github.com/user-attachments/assets/9b712cd3-1529-4e1f-b7b4-beea902e9e42)
	Verify the data looks correct to what was present in KeyPass
	![image](https://github.com/user-attachments/assets/a91fa0cb-f366-4a1a-871a-e854349d9616)

**6. Edit convert-csv-to-jsons.py**
	Add the csv and json file directory you wish to generate
	
	```nano convert-csv-to-jsons.py```

	
![image](https://github.com/user-attachments/assets/1e085cb6-d864-413a-8a7b-9c8d583cf47a)

	```python convert-csv-to-jsons.py```

	
![image](https://github.com/user-attachments/assets/079c9e6a-956f-43ef-912e-471b9c2b1e5a)


**8. Now there's an individual json file for each customer to be imported to OP**
   	
![image](https://github.com/user-attachments/assets/6d67e5ed-b8d8-4acd-be97-846c897a313b)


**9. You can adjust permissions to push to the customer vault via editing powershell-op-import-single-customer.ps1**
	Add appropiate Emails and Group Names respectively
	
![image](https://github.com/user-attachments/assets/61684688-c9ee-4dca-aa81-97b2ec85727e)

**10. Pushing to OP >**
move the customer json files to a folder you can access via powershell and this command will cycle through that given directory for every json file and import.
each import can take a few seconds. you'll be prompted by OnePass to authorise op to proceed. each entry takes a minute or two - 
```Get-ChildItem -Path ".\example_customers\" -Filter "*.json" | ForEach-Object { ./powershell-op-import-single-customer.ps1 $_.FullName }```

![image](https://github.com/user-attachments/assets/96961bcc-e16f-4afd-83c6-a7ed4192ec06)



**In Action**

**Powershell cycling through JSONs**


https://github.com/user-attachments/assets/a4dbad2a-db28-47be-b8a5-35d554a10b31



**1Password items being included within vault**





https://github.com/user-attachments/assets/89b062d6-cafe-400d-893b-46dcc66593b3






