// Linked list of transport card records implementation ... Assignment 1 COMP9024 18s2
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include "cardLL.h"
#include "cardRecord.h"

// linked list node type
// DO NOT CHANGE
typedef struct node {
    cardRecordT data;
    struct node *next;
} NodeT;

// linked list type
typedef struct ListRep {
   NodeT *head;

/* Add more fields if you wish */

} ListRep;

/*** Your code for stages 2 & 3 starts here ***/

// Time complexity: O(1) 
// Explanation: function newLL() sets up an empty list.
//				Its time complexity is a constant which not influenced by input.
List newLL() {
	List L = malloc(sizeof(ListRep));	//O(1)
	L->head = NULL; 					//O(1)
   return L;							//O(1)
}

// Time complexity: O(n)
// Explanation: dropLL(List) removes unwanted list.
//				Its time complexity has a linear relationship with input,
//				as it needs to traversal all elements in the list.
void dropLL(List listp) {
	NodeT *curr = listp->head;			//O(1)
	// while listp still has elements, release curr and move curr to next
	while(curr != NULL){				//O(n)
		NodeT *temp = curr->next;		//O(n)
		free(curr);						//O(n)
		curr = temp;					//O(n)
	}
	// release last element in listp
	free(listp);						//O(1)
}

// Time complexity: O(n)
// Explanation: removeLL(List, int) finds and removes card record.
//				Its time complexity has a linear relationship with input.
//				Because it may need to traversal all elements in the list.
void removeLL(List listp, int cardID) {
	// curr4: a pointer at current node(from head of listp)
	// temp2: a pointer at last node of curr4
	NodeT *curr4 = listp->head;			//O(1)
	NodeT *temp2 = listp->head;			//O(1)
	int c = 0;							//O(1)
	// if listp is empty
	if(curr4 == NULL){					//O(1)
		printf("Card not found.\n");	//O(1)
		return;							//O(1)
	}
	// compare cardID with curr4->data.cardID itetatively
	// break when find same cardID,
	// or reach end of listp
	while(curr4->next != NULL && curr4->data.cardID != cardID){		//O(n)
		temp2 = curr4;												//O(n)
		curr4 = temp2->next;										//O(n)
		c++;														//O(n)
	}	
	// if listp only has one element and is cardID
	if(curr4->data.cardID == cardID && curr4->next == NULL && c == 0){	//O(1)
		listp->head = NULL;				//O(1)
		return;							//O(1)
	}
	// if listp has more than one element and 1st is cardID
	if(curr4->data.cardID == cardID && c == 0){		//O(1)
		listp->head = curr4->next;					//O(1)
		return;										//O(1)
	}
	// if cardID found
	if(curr4->data.cardID == cardID){	//O(1)
		temp2->next = curr4->next;		//O(1)
		return;							//O(1)
	}
	// cardID not found
	printf("Card not found.\n");		//O(1)
	return;								//O(1)
}

// Time complexity: O(n)
// Explanation: insertLL(List, int, float) insert in ascending order
//				(if cardID new), else update card balance.
//				Its time complexity has a linear relationship with input.
//				Because it may need to traversal all elements in the list.
void insertLL(List listp, int cardID, float amount) {
	// pointer *new is the new node needs to be inserted
	NodeT *new = malloc(sizeof(NodeT));		//O(1)
	assert(new != NULL);					//O(1)
	new->data.cardID = cardID;				//O(1)
	new->data.balance = amount;				//O(1)
	// curr1 is pointer at list head
	NodeT *curr1 = listp->head;				//O(1)
	// if listp is empty,
	// or cardID smaller than curr1->data.cardID
	if(curr1 == NULL || cardID < curr1->data.cardID){	//O(1)
		listp->head = new;					//O(1)
		new->next = curr1;					//O(1)
		printf("Card added.\n");			//O(1)
		return;								//O(1)
	}
	// traversal the listp until
	// reach the end of listp,
	// or cardID larger than curr1->data.cardID
	NodeT *temp1;							//O(1)
	while(curr1->next != NULL && cardID > curr1->data.cardID){	//O(n)
		temp1 = curr1;						//O(n)
		curr1 = temp1->next;				//O(n)
	}
	// if cardID equal to curr1->data.cardID
	if(cardID == curr1->data.cardID){		//O(1)
		curr1->data.balance = curr1->data.balance + amount;	//O(1)
		printCardData(curr1->data);			//O(1)
		return;								//O(1)
	}
	// if cardID less than curr1->data.cardID
	if(cardID < curr1->data.cardID){		//O(1)
		temp1->next = new;					//O(1)
		new->next = curr1;					//O(1)
		printf("Card added.\n");			//O(1)
		return;								//O(1)
	}
	// else, insert the new node in the end of listp
	curr1->next = new;						//O(1)
	new->next = NULL;						//O(1)
	printf("Card added.\n");				//O(1)
	return;									//O(1)
}

// Time complexity: O(n)
// Explanation: getAverageLL(List, int *, float *) gets #cards, average balance
//				Its time complexity has a linear relationship with input,
//				as it needs to traversal all elements in the list. 
void getAverageLL(List listp, int *n, float *balance) {
	int count = 0;								//O(1)
	float total_balance = 0;					//O(1)
	// use pointer curr2 traversal the listp
	NodeT *curr2 = listp->head;					//O(1)
	while(curr2 != NULL){						//O(n)
		count++;								//O(n)
		total_balance += curr2->data.balance;	//O(n)
		curr2 = curr2->next;					//O(n)
	}
	n[0] = count;							//O(1)
	if(count == 0){							//O(1)
		balance[0] = 0;						//O(1)
		return;								//O(1)
	}
	total_balance = total_balance / count;	//O(1)
	balance[0] = total_balance;				//O(1)
   return;									//O(1)
}

// Time complexity: O(n)
// Explanation: showLL(List) displays all card records in list
//				Its time complexity has a linear relationship with input,
//				as it needs to traversal all elements in the list. 
void showLL(List listp) {
	NodeT *curr3 = listp->head;				//O(1)
	while(curr3 != NULL){					//O(n)
		printCardData(curr3->data);			//O(n)
		curr3 = curr3->next;				//O(n)
	}
   return;									//O(1)
}
