#include<stdio.h>
#include<stdlib.h>
#include<string.h>

struct stud{
  int PRN;
  char name[20];
  char pos;
  char year[10];
  struct stud *next;
};

void create(struct stud *H){
  struct stud *temp = H;
  struct stud *curr;
  char ch;
  do{
      struct stud *curr=(struct stud *) malloc(sizeof(struct stud));
      printf("\n Enter details as follows -> PRN, Name, Pos(char), year :- \n");
      scanf("%d%s %c%s",&curr->PRN, curr->name, &curr->pos,curr->year);
      curr -> next = NULL;
      temp -> next = curr;
      temp = curr;
      printf("\nEnter Y for next or N for display :");
      scanf(" %c",&ch);
      }while(ch =='y' || ch =='Y');
      
      
  }

struct stud* createNewList() {
    struct stud *newList = (struct stud*)malloc(sizeof(struct stud));
    newList->next = NULL;
    create(newList); // You can use your existing create function to populate the new list
    return newList;
}
  
void display(struct stud *H){
  if(H->next==NULL){
    printf("\nList is Empty");
    }
  else{
  	struct stud *temp = H ->next;
  	printf("PRN\tName\tPos\tYear");
  	while(temp != NULL){
  	  printf("\n%d\t%s\t %c\t%s", temp->PRN, temp->name, temp->pos, temp->year);
  	  temp = temp ->next;
  	}
  }  
  }
  
int length(struct stud *H){
  int i=0;
  struct stud *curr;
  curr = H -> next;
  while(curr != NULL){
    i++;
    curr = curr -> next;
  }
  printf("\nNumber of nodes:%d",i);
  return i;
}

void insert(struct stud *H) {
    int pos1, i = 1;
    struct stud *curr = H;
    int k = length(H);
    printf("\nEnter the pos to be inserted: ");
    scanf("%d", &pos1);

    struct stud *nnode = (struct stud *)malloc(sizeof(struct stud));
    printf("\nEnter details (PRN, Name, Pos(char), Year): ");
    scanf("%d%s %c%s", &nnode->PRN, nnode->name, &nnode->pos, nnode->year);

    if (pos1 == 1) {
        // Insert at the beginning with position "president" (p)
        nnode->next = H->next;
        H->next = nnode;

        // Adjust the position of the former first node to "member" (m)
        if (H->next->next != NULL) {
            H->next->next->pos = 'm';
        }
    } else if (pos1 == k + 1) {
        // Insert at the end with position "secretary" (s)
        while (curr->next != NULL) {
            curr = curr->next;
        }
        curr->next = nnode;
        nnode->next = NULL;
        nnode->pos = 's';
    } else if (pos1 > 1 && pos1 < k + 1) {
        // Insert in the middle
        while (curr != NULL && i < pos1 - 1) {
            i++;
            curr = curr->next;
        }
        nnode->next = curr->next;
        curr->next = nnode;
    } else {
        printf("Invalid Position");
        free(nnode);
    }
}


void delete(struct stud *H) {
    int pos;
    printf("\nEnter the position of the node to be deleted :-  ");
    scanf("%d", &pos);

    int currentPos = 1;
    struct stud *prev = H;
    struct stud *curr = H->next;
     struct stud *temp;
    
    int k = length(H);
    if(k < pos){
        printf("Invalid position");
        return;
    }
    else {
        while(currentPos < pos && curr != NULL){
            currentPos++;
            prev = curr;
        curr = curr->next;
        }
        temp = curr;
        prev->next = curr->next;
        curr->next = NULL;
        free(temp);
    }

    printf("Node at position %d not found in the list.\n", pos);
}

void reverse(struct stud *H) {
    struct stud *prev = NULL;
    struct stud *curr = H->next;
    struct stud *nextNode = NULL;

    while (curr != NULL) {
        nextNode = curr->next;
        curr->next = prev;
        prev = curr;
        curr = nextNode;
    }

    // Update the head's next pointer to the new first node
    H->next = prev;
}

void sort(struct stud *H) {
    struct stud *curr = H->next;
    struct stud *temp;
    int swapped;

    do {
        swapped = 0;
        curr = H->next;
        while (curr->next != NULL) {
            if (curr->PRN > curr->next->PRN) {
                // Swap the data fields (PRN, name, pos, year)
                int tempPRN = curr->PRN;
                curr->PRN = curr->next->PRN;
                curr->next->PRN = tempPRN;

                char tempName[20];
                strcpy(tempName, curr->name);
                strcpy(curr->name, curr->next->name);
                strcpy(curr->next->name, tempName);

                char tempPos = curr->pos;
                curr->pos = curr->next->pos;
                curr->next->pos = tempPos;

                char tempYear[10];
                strcpy(tempYear, curr->year);
                strcpy(curr->year, curr->next->year);
                strcpy(curr->next->year, tempYear);

                swapped = 1;
            }
            curr = curr->next;
        }
    } while (swapped);
}

void merge(struct stud *oldList, struct stud *newList) {
    struct stud *temp = oldList;
    while (temp->next != NULL) {
        temp = temp->next;
    }
    temp->next = newList->next;
    free(newList); // Free the memory allocated for the new list
}


int main() {
    struct stud *head = (struct stud*)malloc(sizeof(struct stud));
    head->next = NULL;
    create(head);
    display(head);
    length(head);
    int x;

    while (1) {
        printf("\n1.Insert 2.Delete 3.Sort 4.Merge Lists 5.Display 6.Reverse 0.EXIT\nChoose an operation: ");
        scanf("%d", &x);

        switch (x) {
            case 1:
                insert(head);
                break;
            case 2:
                delete(head);
                break;
            case 3:
                sort(head);
                break;
        
            case 4: {
                struct stud *newList = createNewList();
                merge(head, newList);
		display(head);
                break;
            }
            case 5:
                display(head);
                break;

	    case 6 :
		reverse(head);
		break;

            case 0:
                printf("Exiting the program.\n");
                free(head); // Free the memory allocated for the linked list
                exit(0); // Exit the program
            default:
                printf("Invalid choice\n");
        }
    }

    return 0;
}
