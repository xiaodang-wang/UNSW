/**
     main.c

     Program supplied as a starting point for
     Assignment 1: Transport card manager

     COMP9024 18s2
**/
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <ctype.h>

#include "cardRecord.h"
#include "cardLL.h"

void printHelp();
void CardLinkedListProcessing();

int main(int argc, char *argv[]) {
   if (argc == 2) {

      /*** Insert your code for stage 1 here ***/
      
      int n = atoi(argv[1]);
      // if ./main n, n is a postive int
      if (n > 0){
         // creat a dynamic array on the heap
         cardRecordT *card = malloc( n * (sizeof(float)+sizeof(int)));
         // promote user input valid cardID and amount n times
         for(int i=0; i<n; i++){
            /* get valid card id */
            printf("Enter card ID: ");
            card[i].cardID = readValidID();
            while(card[i].cardID == -999){
               printf("Not valid. Enter a valid value: ");
               card[i].cardID = readValidID();
            }
            /* get valid card balance */
            printf("Enter amount: ");
            card[i].balance = readValidAmount();
            while(card[i].balance == -999){
               printf("Not valid. Enter a valid value: ");
               card[i].balance = readValidAmount();
            }
         }
         // print out results
         float total_amount = 0;
         for(int j=0; j<n; j++){
            printCardData(card[j]);
            total_amount += card[j].balance;
         }
         printf("Number of cards on file: %d\n",n);
         float average = total_amount/n;
         if(average < 0)
            printf("Average balance: -$%.2f\n",-average);
         else
            printf("Average balance: $%.2f\n",average);
         free(card);
      }     
   } else {
      CardLinkedListProcessing();
   }
   return 0;
}

/* Code for Stages 2 and 3 starts here */

void CardLinkedListProcessing() {
   int op, ch;
   List list = newLL();   // create a new linked list
   while (1) {
      printf("Enter command (a,g,p,q,r, h for Help)> ");
      do {
	 ch = getchar();
      } while (!isalpha(ch) && ch != '\n');  // isalpha() defined in ctype.h
      op = ch;
      // skip the rest of the line until newline is encountered
      while (ch != '\n') {
	 ch = getchar();
      }
      switch (op) {
         // case a: add a card record
         case 'a':
         case 'A':
            printf("Enter card ID: ");
            int cardID_list = readValidID();
            while(cardID_list == -999){
               printf("Not valid. Enter a valid value: ");
               cardID_list = readValidID();
            }
            printf("Enter amount: ");
            float cardbalance_list = readValidAmount();
            while(cardbalance_list == -999){
               printf("Not valid. Enter a valid value: ");
               cardbalance_list = readValidAmount();
            }
            insertLL(list, cardID_list, cardbalance_list);
	    break;
         // case g: get #card and average balance
         case 'g':
         case 'G':
            printf("Number of cards on file: ");
            int *n,a=0;
            n = &a;
            float *balance, b=0;
            balance = &b;
            getAverageLL(list, n, balance);
            printf("%d\n",*n);
            if(*balance < 0)
               printf("Average balance: $%.2f\n",-*balance);
            else
               printf("Average balance: $%.2f\n",*balance);
	    break;
	    
         case 'h':
         case 'H':
            printHelp();
	    break; 
         // case p: print list 
         case 'p':
         case 'P':
            showLL(list);

	    break;
         // case r: remove card
         case 'r':
         case 'R':
            printf("Enter card ID: ");
            int cardID_r = readValidID();
            while(cardID_r == -999){
               printf("Not valid. Enter a valid value: ");
               cardID_r = readValidID();
            }
            removeLL(list, cardID_r);
	    break;
       
	 case 'q':
         case 'Q':
            dropLL(list);       // destroy linked list before returning
	    printf("Bye.\n");
	    return;
      }
   }
}

void printHelp() {
   printf("\n");
   printf(" a - Add card record\n" );
   printf(" g - Get average balance\n" );
   printf(" h - Help\n");
   printf(" p - Print all records\n" );
   printf(" r - Remove card\n");
   printf(" q - Quit\n");
   printf("\n");
}
