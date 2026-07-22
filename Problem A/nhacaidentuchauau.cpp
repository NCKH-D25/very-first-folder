#include <iostream>

using std::cout;
using std::endl;
using std::cin;

// contains function prototypes for functions srand and rand
#include <cstdlib>
#include <ctime>   // contains prototype for function time

int rollDice(void);  // function prototype

int main()
{
   // enumeration constants represent game status
   enum Status { CONTINUE, WON, LOST };

   int sum;
   int myPoint;
   int choice;

   Status gameStatus;  // can contain CONTINUE, WON or LOST

   // randomize random number generator using current time
   srand(time(0));
   	while (true){
   		cout << "\n===== MENU =====\n";
      cout << "1. Choi game\n";
      cout << "0. Thoat\n";
      cout << "Nhap lua chon: ";
      cin >> choice;

      if (choice == 0) {
         cout << "Game ket thuc!\n";
         break;}
         
   	if (choice==1){
	  // first roll of the dice
	sum = rollDice();
   // determine game status and point based on sum of dice
   switch (sum) {

      // win on first roll
      case 7:
      case 11:
         gameStatus = WON;
         break;

      // lose on first roll
      case 2:
      case 3:
      case 12:
         gameStatus = LOST;
         break;

      // remember point
      default:
         gameStatus = CONTINUE;
         myPoint = sum;
         cout << "Point is " << myPoint << endl;
         break;
   }

   // while game not complete ...
   while (gameStatus == CONTINUE) {
      sum = rollDice();   // roll dice again

      // determine game status
      if (sum == myPoint)
         gameStatus = WON;
      else if (sum == 7)
         gameStatus = LOST;
   }

   // display won or lost message
   if (gameStatus == WON)
      cout << "PLAYER WINS" << endl;
   else
      cout << "PLAYER LOSES" << endl;
} 
	
}
   return 0;  // indicates successful termination
}


// roll dice, calculate sum and display results
int rollDice(void)
{
   int die1;
   int die2;
   int workSum;

   die1 = 1 + rand() % 6;  // pick random die1 value
   die2 = 1 + rand() % 6;  // pick random die2 value
   workSum = die1 + die2;  // sum die1 and die2

   // display results of this roll
   cout << "Player rolled " << die1 << " + " << die2
        << " = " << workSum << endl;

   return workSum;  // return sum of dice
}
