#include <iostream>
#include <string.h>
using namespace std;

class gnode
{
    string name;
    int id;
    gnode *next;
    friend class graph;
};

class graph
{
private:
    gnode *head[20];
    int n;
    int visit[20];

public:
    graph()
    {
        cout << "Number of people? ";
        cin >> n;
        for (int i = 0; i < n; i++)
        {
            head[i] = new gnode;
            cout << "Enter name of person " << i << "\n";
            cin >> head[i]->name;
            head[i]->id = i;
            head[i]->next = NULL;
        }
    }

    void create();
    void display();
    void dfs_r();
    void dfs_r(string v);
    void dfs_nr();
    void bfs();
    int isthere(string fren);
    int where(string fren);
};

class stack
{
    int top;
    string data[30];

public:
    stack()
    {
        top = -1;
    }

    void push(string temp)
    {
        top++;
        data[top] = temp;
    }

    string pop()
    {
        string temp = data[top];
        top--;
        return temp;
    }
    int empty;
    friend class graph;
};

class queue
{
    int front;
    int rear;
    string q[10];

public:
    queue()
    {
        front = -1;
        rear = -1;
    }
    void enqueue(string temp)
    {
        rear++;
        q[rear] = temp;
    }
    string dequeue()
    {
        front++;
        string temp = q[front];
        return temp;
    }
    friend class graph;
};

int graph::isthere(string fren)
{
    for (int i = 0; i < n; i++)
    {
        if (fren == head[i]->name)
        {
            return 1;
        }
    }
    return 0;
}

int graph::where(string fren)
{
    for (int i = 0; i < n; i++)
    {
        if (fren == head[i]->name)
        {
            return i;
        }
    }
}

void graph::create()
{
    string fren;
    char ch;
    for (int i = 0; i < n; i++)
    {
        gnode *temp = head[i];
        do
        {
            cout << "\nEnter friend of " << head[i]->name << ": \n";
            cin >> fren;
            if (fren == head[i]->name)
            {
                cout << "They can't be their own friend!! Try again\n";
            }
            else if (!isthere(fren))
            {
                cout << "No such person exists!!\n";
            }
            else
            {
                gnode *curr = new gnode;
                curr->name = fren;
                curr->id = where(fren);
                curr->next = NULL;
                temp->next = curr;
                temp = temp->next;
            }
            cout << "Are there more adjacent nodes? (y/n): ";
            cin >> ch;

        } while (ch == 'y');
    }
}

void graph::display()
{
    gnode *temp;
    for (int i = 0; i < n; i++)
    {
        temp = head[i];
        cout << "\nFriends of " << temp->name << "\n";
        temp = temp->next;
        while (temp != NULL)
        {
            cout << "-> " << temp->name << "\n";
            temp = temp->next;
        }
    }
}

void graph::dfs_r()
{
    string v;
    for (int i = 0; i < n; i++)
    {
        visit[i] = 0;
    }
    cout << "Please enter name of friend/node you'd like to start with: ";
    cin >> v;
    if (!isthere(v))
    {
        cout << "Please enter a valid node!\n";
    }
    else
    {
        dfs_r(v);
    }
}

void graph::dfs_r(string v)
{
    cout << "\n"
         << v;
    int x = where(v);
    visit[x] = 1;
    gnode *temp = head[x]->next;
    while (temp != NULL)
    {
        string w = temp->name;
        if (!visit[temp->id])
        {
            dfs_r(w);
        }
        temp = temp->next;
    }
}

void graph::dfs_nr()
{
    string v;
    cout << "Please enter name of friend/node you'd like to start with: ";
    cin >> v;
    if (!isthere(v))
    {
        cout << "Please enter a valid node!\n";
    }
    else
    {
        for (int i = 0; i < n; i++)
        {
            visit[i] = 0;
        }
        stack st;
        int x = where(v);
        st.push(v);
        visit[x] = 1;

        do
        {
            v = st.pop();
            cout << "\n"
                 << v;
            x = where(v);
            gnode *temp = head[x]->next;
            while (temp != NULL)
            {
                string w = temp->name;
                int pos = temp->id;
                if (!visit[temp->id])
                {
                    st.push(w);
                    visit[pos] = 1;
                }
                temp = temp->next;
            }

        } while (st.top != -1);
    }
}

void graph::bfs()
{
    queue kyu;
    string v;
    int x;
    cout << "Please enter name of friend/node you'd like to start with: ";
    cin >> v;
    if (!isthere(v))
    {
        cout << "Please enter a valid node!\n";
    }
    else
    {
        for (int i = 0; i < n; i++)
        {
            visit[i] = 0;
        }
        x = where(v);
        kyu.enqueue(v);
        visit[x] = 1;
        do
        {
            v = kyu.dequeue();
            x = where(v);
            cout << "\n"
                 << head[x]->name;
            gnode *temp = head[x]->next;
            while (temp != NULL)
            {
                if (visit[temp->id] == 0)
                {
                    kyu.enqueue(temp->name);
                    visit[temp->id] = 1;
                }
                temp = temp->next;
            }
            if (kyu.rear == kyu.front)
            {
                break;
            }
        } while (1);
    }
}

int main()
{
    graph gp;
    string stri;
    int choice;
    gp.create();
    do
    {
        cout << "\n\n*******************\n";
        cout << "What would you like to do? \n1. DFS Recursive \n2. DFS Non-Recursive \n3. BFS \n4. Display all friends \n5. Exit\nEnter choice: ";
        cin >> choice;
        switch (choice)
        {
        case 1:
            cout << "\n\nRecursive Depth First Traversal... \n";
            gp.dfs_r();
            break;

        case 2:
            cout << "\n\nNon-recursive Depth First Traversal... \n";
            gp.dfs_nr();
            break;

        case 3:
            cout << "\n\nBreadth First Traversal... \n";
            gp.bfs();
            break;

        case 4:
            cout << "\n\nDisplaying all friends... \n";
            gp.display();
            break;

        case 5:
            break;

        default:
            cout << "\nPlease choode from the menu!\n";
            break;
        }
    } while (choice != 5);
}