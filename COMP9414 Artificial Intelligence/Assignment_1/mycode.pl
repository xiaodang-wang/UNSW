% Full Name: Xiaodan Wang
% Student Number: Z5145114
% Assignment Name: Assignment 1 - Prolog Programming

% Q1
% sumsq_neg(Number, Sum) -Sum is the sum of squares of negtive numbers in Number
% 	Number is a list 
% e.g.
% ?- sumsq_neg([1,-3,-5,2,6,8,-2], Sum).
% Sum = 38;
% false

% base case, Number list is empty
sumsq_neg([],0).

% recursive
% For negtive numbers, do the square and add in sum. Then recursive sumsq_neg.
sumsq_neg([Head | Tail], Sum) :-
	Head < 0,
	sumsq_neg(Tail, Sum_1),
	Sum is Head * Head + Sum_1.

% For positive numbers and zero, recursive sumsq_neg.
sumsq_neg([Head | Tail], Sum) :-
	Head >= 0,
	sumsq_neg(Tail, Sum).

% Q2
% all_like_all(Who_List, What_List) -Everyone in Who_List likes every item in What_List
%	Base on likes facts
% e.g.
% ?- all_like_all([jane,tim],[apple,mango]).
% true ;
% false.

% base case, Who_List is empty
all_like_all([],_).

% recursive 
% use someone_likes_something predict check everyone in Who_List
all_like_all([Head | Tail], What_List) :-
	someone_likes_something(Head, What_List),
	all_like_all(Tail, What_List).

% someone_likes_something(Name, What_List) -Succeed if Name likes every item in What_List
% e.g.
% ?- someone_likes_something(tim, [apple, mango]).
% true;
% false.
% ?- someone_likes_something(mary, [apple, mango]).
% false.

% base case
someone_likes_something(_,[]).

% recursive
% find out all items Name likes and put them into Likes_List
% check is everything in What_List in Likes_List
someone_likes_something(Name, [Head | Tail]):-
	someone_likes_something(Name, Tail),
	findall(Fruit, likes(Name, Fruit), Likes_List),
	member(Head, Likes_List).

% Q3
% sqrt_table(N, M, Result) -Result is a list of number and its square root from N down to M
%	M and N are non-negative integers
%	n >= M
% e.g.
% ?-sqrt_table(7, 4, Result).
% Result = [[7, 2.6457513110645907], [6, 2.449489742783178], [5, 2.23606797749979], [4, 2.0]] ;
% false.
% ?- sqrt_table(7, 8, Result).
% false.

% base case
sqrt_table(M, M, [[M, Sqrt_M]]) :-
	Sqrt_M is sqrt(M).

% recursive
% From N to M, do sqrt
sqrt_table(N, M, [[N_2, Sqrt] | Result_1]) :-
	N >= M,
	N_1 is N - 1,
	sqrt_table(N_1, M, Result_1),	
	Sqrt is sqrt(N_1 + 1),
	N_2 is N_1 + 1.

% Q4
% suc(+Original_list, -Successive_list, -Rest_list) -judge a sequence of successive increasing
% 	numbers from the begin of Original_list, and save the first and last number of sequence 
%	in Successive_list. As well as, save the rest of Original_list into Rest_list.
% e.g.
% ?- suc([1,2,3,5,6,8,10], Successive, Rest).
% Successive = [1,3]
% Rest = [5,6,8,10];
% false.
% ?- suc([5,6,8,10], Successive, Rest).
% Successive = [5,6]
% Rest = [8,10];
% false.
% ?- suc([8,10], Successive, Rest).
% Successive = 8
% Rest = [10];
% false.
% ?- suc([10], Successive, Rest).
% Successive = 10
% Rest = [];
% false.

% base case 1
% Original_list only has one number, it must be alone. 
% So Successive_list is this number, and Rest_list is empty.
suc([X], X, []).

% base case 2
% Original_list only has two successive numbers. 
% Successive_list is these numbers, and Rest_list is empty.
suc([X1, X2], [X1 | [X2]], []) :-
	1 =:= X2 - X1.

% recursive
% Original_list begins with three successive numbers.
% Save first number into first place of Successive_list.
% Generate a new Original_list which begin with second, third numbers and rest of Original_list.
% Do recursive till reach one base case.
suc([X1, X2 ,X3| Tail], [X1 | Successive_2], Tail_2) :- 
	1 =:= X2 - X1,
	1 =:= X3 - X2,
	suc([X2, X3 | Tail], [_ | Successive_2], Tail_2).

% base case 3
% Original_list begins with three numbers, which the first and second numbers are successive
% increasing as well as second number and third number are not successive.
% So it is the end of successive increasing sequence.
% Save first and second numbers into Successive_list.
% Return third number and rest of Original_list as a new Rest_list.
suc([X1, X2 ,X3| Tail], [X1 | [X2]], [X3 | Tail]) :- 
	1 =:= X2 - X1,
	1 =\= X3 - X2.

% base case 4
% Original_list begins with two unsuccessive increasing numbers.
% Return the first number as Successive_list. 
% Second number with rest of Original_list is Rest_list.
suc([X1 ,X2 | Tail], X1, [X2 | Tail]) :-
	1 =\= X2 - X1.

% chop_up(List, NewList) -chop up the List into NewList
%	all sequence of successive increasing numbers replaced by two-item list containing first and last number
% e.g.
% ?- chop_up([9,10,5,6,7,3,1], Result).
% Result = [[9, 10], [5, 7], 3, 1] ;
% false.

% base case
chop_up([],[]).

% recursive
% For List, do suc, return first and last numbers [A ,B] 
% of successive increasing sequence and rest list.
% For rest list, do suc again.
% Until the rest list is empty.
chop_up(List, [Successive | Result_1]) :-
	suc(List, Successive, Tail_2),
	chop_up(Tail_2, Result_1).


% Q5
% tree_eval(+Value, +Tree, -Eval) -Eval is the result of evaluating the expression-tree Tree with z
%	Variable z set equal to Value
% e.g.
% ?- tree_eval(2, tree(tree(empty,z,empty),
%                 	  '+',tree(tree(empty,1,empty),
%						  '/',tree(empty,z,empty))), Eval).
% Eval = 2.5 ;
% false.

% base case 1
tree_eval(Z, tree(empty, z, empty), Z).

% base case 2
tree_eval(_, tree(empty, N, empty), N) :-
	number(N).

% recursive for +
tree_eval(Z, tree(Left, '+', Right), Eval) :-
	tree_eval(Z, Left, L_Eval),
	tree_eval(Z, Right, R_Eval),
	Eval is L_Eval + R_Eval.

% recursive for -
tree_eval(Z, tree(Left, '-', Right), Eval) :-
	tree_eval(Z, Left, L_Eval),
	tree_eval(Z, Right, R_Eval),
	Eval is L_Eval - R_Eval.

% recursive for *
tree_eval(Z, tree(Left, '*', Right), Eval) :-
	tree_eval(Z, Left, L_Eval),
	tree_eval(Z, Right, R_Eval),
	Eval is L_Eval * R_Eval.

% base case 3
% for zero divisor
tree_eval(_, tree(_, '/', tree(empty,0,empty)), _) :-
	write('wrong input'),!,fail.

% recursive for /
tree_eval(Z, tree(Left, '/', Right), Eval) :-
	tree_eval(Z, Left, L_Eval),
	tree_eval(Z, Right, R_Eval),
	Eval is L_Eval / R_Eval.
