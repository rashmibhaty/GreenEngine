# GreenEngine
**What's the problem?**

Reduce, Reuse, Recycle are the key concepts that can be used to protect our environment. Sustainable ways to dispose household materials, that is of no use anymore, is a much-needed step. To attract larger audience to follow sustainable solution, a well-organized way of disposing materials is important. There is also a need to improve the reuse of unused materials (clothes, utensils, books, toys, etc.).  

**How can technology help?**

Local governing bodies do have arrangements to collect unused household materials. But sometimes we have restrictions on how frequently collection drives happen or materials that will be collected. It does not have any rewarding mechanism for the reusable/recyclable materials that we provide. Also, giving materials to ragpickers does not seem to be a reliable option. Given the situation, introducing an online website to facilitate collection and disposal of any kind of materials whenever we have something to dispose through an authorized media is required.

**The idea**

•	An online website to arrange collection/pick up of unused household materials.

•	An agency (NGO/any organization) to collect and dispose these materials in a sustainable way. 

•	Reselling of reusable things via shops at reasonable prices to needy.

•	Rewarding mechanism to the users based on the quantity and quality of the materials given. 


**Demo Video**
-link


**The architecture**

-	![architecture](https://user-images.githubusercontent.com/65997817/122563853-58325c80-d062-11eb-9f90-57cd17a5519e.png)


**User side:**

1.	The user registers to the site and login with the credential.
2.	The user chooses the category of materials that need to be disposed and the preferred date and time slot to schedule the pick-up.
3.	The user submits the pick-up request and a confirmation SMS with a unique booking number is send to the user with the registered mobile number.
4.	Refer the Agent side section 
5.	Once the agent enters the pick-up details, user can view the order summary and the reward points received.

**Agent side:**

1.	Agent gets the pick-up SMS notification once the user schedules a pick-up.
2.	Agent picks up the materials in the scheduled date-time slot.
3.	The agent will login to the site using the agent login credentials.
4.	The agent will measure the quantity of each category of materials collected and make an entry in the site along with the unique booking number for that pick-up.
5.	Based on the quantity entered, the user will be credited reward points that can be redeemed.

**Cloud side:**
1.	We run IBM Cloud Foundy App using Flask written in Python
2.	We use IBM Cloudant data base for storing all data
3.	We use Twilio SMS service

**Project RoadMap**

	Current features
	
1.	Currently the site has user login and agent login. 
2.	Using user login, users can register, and the registered users can schedule a pick-up of materials (plastic, clothes, e-waste, paper etc.) at their preferred date-time slot.
3.	Agents will use agent login to enter the details of the collected materials (particularly the quantity of each category of items collected) for each of the pick-up. 
4.	Using the details entered by agent for each pick-up, a reward mechanism is introduced were the user will get reward points that can be redeemed.
5.	SMS service is incorporated with the help of Twilio to send booking confirmation message to the user and pick-up notification to agent.

        Future enhancements
	
1.	Scheduling algorithm for pick-up based on location.
2.	Better rewarding schemes to users based on the quality of the materials.
3.	Targeting more users based on machine learning algorithms.
4.	Establishing a channel to reuse materials like shop, online website, etc. 


**Live Demo**

https://newapp-hilarious-puku-ss.eu-gb.mybluemix.net/

**Built With **

•	IBM Cloudant - The NoSQL database us

•	CloudFoundry

•	Twilio   etc…

