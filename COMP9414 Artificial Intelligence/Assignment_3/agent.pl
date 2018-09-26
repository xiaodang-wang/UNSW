% agent.pl
% written by Xiaodan Wang
% for COMP9414 Assignment 3 - Option 2 Prolog BDI agent
%
%
%
%
%

% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% Q1
% generate initial intentions at first
%
% 		initial_intentions(-Intentions) 
%          -Intentions is intents(L,[])
% 			L in the form [[goal(X1,Y1),[]],...[goal(Xn,Yn),[]]]
% 			(Xn,Yn) is the location of monster
% 			(X1,Y1)... are the location of stones need to be dropped 
% 			from the agent current location to monster
% 			mininum stones dropped
%
% using ucsdijkstra and pathsearch to find the mininum path to monster:
% solve((Xagent, Yagent), Intents, _, _).
% modify Intents into Intents2(L form):
% intentions_generate(Intents, -Intents2).
% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %

initial_intentions(intents(Intents1,[])) :-
	agent_at(Xagent, Yagent),
	solve((Xagent, Yagent), Intents, _, _),
	intentions_generate(Intents, Intents1).

% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% 		intentions_generate(+Intents, -Intents1) 
%          -Intents is a path to monster
% 			in the form of [(X1,Y1),...(Xn,Yn)]
% 			Intents2 is a list of where stones need to be dropped
%
% if (X,Y) is in land, leave it 
% if (X,Y) not in land, add it into Intents1
% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %

% base case
intentions_generate([], []).

% recursive part 
% (X,Y) is not in land
intentions_generate([(Xpath, Ypath)|Tail], Intentions) :-
	land(Xpath, Ypath),
	intentions_generate(Tail, Intentions).

% (X,Y) is land, add into Intents1
intentions_generate([(Xpath, Ypath)|Tail], Intents1) :-
	not(land(Xpath, Ypath)),
	intentions_generate(Tail, Intentions),
	append(Intentions, [[goal(Xpath,Ypath),[]]], Intents1).

% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% s() is the node expand algorithm for ucsdijkstra
% 
% 		s(+Node, -SuccessorNode, -Cost) 
%          -Node is current node
% 			SuccessorNode is next node can be expanded
%			Cost is the costs to next node
% 
% from (X,Y), the agent could move to (X+1,Y), (X-1,Y), (X,Y+1), (X,Y-1)
% if next node is land, Cost is 0
% else Cost is 1
% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %

s((Xmoment,Ymoment), (Xnext,Ynext), Cost) :-
	Xnext is Xmoment + 1,
	Ynext is Ymoment,
	land(Xnext,Ynext) ->
		Cost = 0;
		Xnext is Xmoment + 1,
		Ynext is Ymoment,
		Cost = 1.

s((Xmoment,Ymoment), (Xnext,Ynext), Cost) :-
	Xnext is Xmoment - 1,
	Ynext is Ymoment,
	land(Xnext,Ynext) ->
		Cost = 0;
		Xnext is Xmoment - 1,
		Ynext is Ymoment,
		Cost = 1.

s((Xmoment,Ymoment), (Xnext,Ynext), Cost) :-
	Xnext is Xmoment,
	Ynext is Ymoment + 1,
	land(Xnext,Ynext) ->
		Cost = 0;
		Xnext is Xmoment,
		Ynext is Ymoment + 1,
		Cost = 1.

s((Xmoment,Ymoment), (Xnext,Ynext), Cost) :-
	Xnext is Xmoment,
	Ynext is Ymoment - 1,
	land(Xnext,Ynext) ->
		Cost = 0;
		Xnext is Xmoment,
		Ynext is Ymoment - 1,
		Cost = 1.

% find the position of monster and set it as the goal
goal((Xgoal, Ygoal)) :-
	monster(Xgoal, Ygoal).

% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% Q2
% converts the stones position into goal list
%
% 		trigger(+Percepts, -Goals) 
%          -Precepts is a list of stones position
% 			in the form stone(X,Y)
% 			Goals is a corresponding list of goals in the form goal(X,Y)
% 		e.g.
% 		?- trigger([stone(1,2),stone(3,4)], Goals).
% 		Goals = [goal(1,2),goal(3,4)].
%
% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %

% base case
trigger([], []).

% recursive part 
trigger([stone(Xpecepts,Ypercepts)|Tail], G1) :-
	trigger(Tail, Goal),
	append([goal(Xpecepts,Ypercepts)], Goal, G1).

% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% Q3
% evaluate goal(X,Y) in Goals 
% if reachable, update it in Intentions
%
% 		incorporate_goals(+Goals, +Intentions, -Intentions1)
% 		   -Precepts is a list of stones position
% 			in the form stone(X,Y)
% 			Goals is a corresponding list of goals in the form goal(X,Y)
% 		e.g.
% 		?- incorporate_goals([goal(1,2)], intents([[goal(9,9),[]]],[]), Intentions1).
% 		Intentions1 = intents([[goal(9, 9), []]], [[goal(1, 2), []]]) .
% 		?- incorporate_goals([goal(1,2)], intents([[goal(9,9),[]]],[[goal(7,8),[]]]), Intentions1).
% 		Intentions1 = intents([[goal(9, 9), []]], [[goal(7, 8), []], [goal(1, 2), []]]) .
% 		?- incorporate_goals([goal(1,2)], intents([[goal(9,9),[drop(9,9)]]],[]), Intentions1).
% 		Intentions1 = intents([[goal(9, 9), [drop(9,9)]]], [[goal(1, 2), []]]) .
%
% using insert_goals() to generate Intentions INT_PICK part
% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %

incorporate_goals(Goals, intents(Intents, Intents_pick), intents(Intents, Int_pick_goals)) :-
	insert_goals(Goals, Intents_pick, Int_pick_goals,[]).

% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% 		insert_goals(+Goals, +Int_pick, -Updated_int_pick, +Temporary)
% 		   -Goals is a list of goal(X,Y) 
% 			Int_pick is the second part of Intentions in the form of [[goal(X, Y), [Plan]],...]
% 			Updated_int_pick is updated
% 		e.g.
% 		?- insert_goals([goal(1,2)], [], Updated_int_pick, []).
% 		Updated_int_pick = [[goal(1, 2), []]] .
% 		?- insert_goals([goal(1,2)], [[goal(7,8),[]]], Updated_int_pick, []).
% 		Updated_int_pick = [[goal(7, 8), []], [goal(1, 2), []]] .
% 		?- insert_goals([goal(1,2)], [], Updated_int_pick, []).
% 		Updated_int_pick = [[goal(1, 2), []]] .
%
% Temporary is a list contains elements whose valid path is shorter than current goals
% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %

% base case: empty Goals 
% Update_int_pick = [Goals2 | Int_pick]
insert_goals([], I, Goals1, Goals2):-
	append(Goals2, I, Goals1).

% recursive part: empty Int_pick 
% evaluate first goal(X,Y)
% if reachable, 
% recursive 'insert_goals(+Goals_left, +[[First_goal,[]]], -Updated_int_pick, +Temporary)'
% else, recursive 'insert_goals(+Goals_left, +[], -Updated_int_pick, +Temporary)'
insert_goals([goal(Xgoal1, Ygoal1)|T1], [], Goals1, Goals2) :-
	agent_at(Xagent, Yagent),
	valid_path2((Xagent, Yagent),(Xgoal1, Ygoal1),_, Ig1, _), !,	
	Ig1 = 1 ->
		insert_goals(T1, [[goal(Xgoal1, Ygoal1),[]]], Goals1, Goals2);
		insert_goals(T1, [], Goals1, Goals2).

% recursive part: goal(X,Y) is already in Int_pick
insert_goals([goal(Xgoal1, Ygoal1)|T1], [[goal(Xgoal2, Ygoal2),T3]|T2], Goals1, Goals2) :-
	not(goal_not_in((Xgoal1, Ygoal1), Goals2)),
	append(Goals2, [[goal(Xgoal2, Ygoal2),T3]|T2], List5),
	insert_goals(T1, List5, Goals1, []).

% recursive part: goal(X,Y) is already in Int_pick
insert_goals([goal(Xgoal1, Ygoal1)|T1], [[goal(Xgoal2, Ygoal2),T3]|T2], Goals1, Goals2) :-
	not(goal_not_in((Xgoal1, Ygoal1), [[goal(Xgoal2, Ygoal2),T3]|T2])),
	append(Goals2, [[goal(Xgoal2, Ygoal2),T3]|T2], List5),
	insert_goals(T1, List5, Goals1, []).

% recursive part: goal(X,Y) is already in Int_pick
insert_goals([goal(Xgoal1, Ygoal1)|T1], [[goal(Xgoal2, Ygoal2),T3]|T2], Goals1, Goals2) :-
	(Xgoal1, Ygoal1) = (Xgoal2, Ygoal2),
	append(Goals2, [[goal(Xgoal2, Ygoal2),T3]|T2], List5),
	insert_goals(T1, List5, Goals1, []).

% recursive part: goal(X,Y) is not reachable
insert_goals([goal(Xgoal1, Ygoal1)|T1], [[goal(Xgoal2, Ygoal2),T3]|T2], Goals1, Goals2) :-
	agent_at(Xagent, Yagent),
	valid_path2((Xagent, Yagent),(Xgoal1, Ygoal1),_, 0, _),!,
	append(Goals2, [[goal(Xgoal2, Ygoal2),T3]|T2], List5),
	insert_goals(T1, List5, Goals1, []).

% recursive part: goal(X,Y) need to be update in Int_pick
% if valid path length of first goal(X1,Y1) in Goals 
% 	> valid path length of first goal(X2,Y2) in Int_pick
% put goal(X2,Y2) into Temporary
% recursive 'insert_goals(+Goals, +Int_pick_left, -Updated_int_pick, +Temporary)'
% else recursive 'insert_goals(+Goals_left, +Int_pick_add_new_goal, -Updated_int_pick, +[])'
insert_goals([goal(Xgoal1, Ygoal1)|T1], [[goal(Xgoal2, Ygoal2),T3]|T2], Goals1, Goals2) :-
	(Xgoal1, Ygoal1) \= (Xgoal2, Ygoal2),
	goal_not_in((Xgoal1, Ygoal1), Goals2),
	agent_at(Xagent, Yagent),
	valid_path2((Xagent, Yagent),(Xgoal1, Ygoal1),_, 1, Len1),!,
	valid_path2((Xagent, Yagent),(Xgoal2, Ygoal2),_, _, Len2),!,
	Len2 >= Len1 ->
 	append([[goal(Xgoal1, Ygoal1), []]], [[goal(Xgoal2, Ygoal2),T3]|T2], List1),
 	append(Goals2, List1, List2),
 	insert_goals(T1, List2, Goals1, []);
	append(Goals2, [[goal(Xgoal2, Ygoal2),T3]], List3),
	insert_goals([goal(Xgoal1, Ygoal1)|T1], T2, Goals1, List3).


% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% goal_not_in is a function to judge whether (X,Y) in a intents list
%
% 		goal_not_in((X,Y), [[goal(Xe, Ye),_]|T])
% 		   -List is in the form of [[goal(Xe, Ye),[]],...]
% 		e.g.
% 		?- goal_not_in((1,2), [[goal(8,6),[drop(8,6)]],[goal(9,9),[]]]).
% 		true .
% 		?- goal_not_in((9,9), [[goal(8,6),[drop(8,6)]],[goal(9,9),[]]]).
% 		false.
%
% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %

% base case
goal_not_in((_,_), []).

% recursive part
goal_not_in((Xg,Yg), [[goal(Xe, Ye),_]|T]) :-
	(Xg,Yg) \= (Xe, Ye),
	goal_not_in((Xg,Yg), T).

% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% s1() is the node expand algorithm for ucsdijkstra1
% 
% 		s1(+Node, -SuccessorNode, -Cost) 
%          -Node is current node
% 			SuccessorNode is next node can be expanded
%			Cost is the costs to next node
% 
% from (X,Y), the agent could move to (X+1,Y), (X-1,Y), (X,Y+1), (X,Y-1)
% if next node is land or has dropped a stone, Cost is 0
% else Cost is 1
% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %

s1((Xmoment,Ymoment), (Xnext,Ynext), Cost) :-
	Xnext is Xmoment + 1,
	Ynext is Ymoment,
	land_or_dropped(Xnext,Ynext) ->
		Cost = 0;
		Xnext is Xmoment + 1,
		Ynext is Ymoment,
		Cost = 1.

s1((Xmoment,Ymoment), (Xnext,Ynext), Cost) :-
	Xnext is Xmoment - 1,
	Ynext is Ymoment,
	land_or_dropped(Xnext,Ynext) ->
		Cost = 0;
		Xnext is Xmoment - 1,
		Ynext is Ymoment,
		Cost = 1.

s1((Xmoment,Ymoment), (Xnext,Ynext), Cost) :-
	Xnext is Xmoment,
	Ynext is Ymoment + 1,
	land_or_dropped(Xnext,Ynext) ->
		Cost = 0;
		Xnext is Xmoment,
		Ynext is Ymoment + 1,
		Cost = 1.

s1((Xmoment,Ymoment), (Xnext,Ynext), Cost) :-
	Xnext is Xmoment,
	Ynext is Ymoment - 1,
	land_or_dropped(Xnext,Ynext) ->
		Cost = 0;
		Xnext is Xmoment,
		Ynext is Ymoment - 1,
		Cost = 1.

% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% valid_path(), valid_path1(), valid_path2(), valid_path3()
% are a series function to calculate whether goal(X,Y) is reachable and if yes how much moves does it take
% 
% 		valid_path2(+(X1, Y1), +(X2, Y2), -Valid_path, -Insert_goal, -Len) 
%          -(X1, Y1) is agent position
% 			(X2, Y2) is goal postion
% 			Valid_path is the shortest valid path from (X1, Y1) to (X2, Y2)
%			Insert_goal is 1 if (X1, Y1) reachable, or it is 0
% 			Len is the length of Valid_path
%
% valid_path2() is used for calculate Len
% valid_path() generates a path from (X1, Y1) to (X2, Y2) by useing ucsdijkstra algorithm
% valid_path1() judges whether the path is valid
% valid_path3() is for cut first result
% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %

valid_path((X1, Y1), (X2, Y2), Valid_path, G) :-
	retractall(goal1(_)),
	assert(goal1((X2,Y2))),
	solve1((X1, Y1), Valid_path, G, _).

valid_path3((X1, Y1), (X2, Y2), Valid_path, G) :-
	valid_path((X1, Y1), (X2, Y2), Valid_path, G), !.

valid_path1((X1, Y1), (X2, Y2), Valid_path, 1) :-
	valid_path3((X1, Y1), (X2, Y2), Valid_path, G),
	G = 0.

valid_path1((X1, Y1), (X2, Y2), Valid_path, 1) :-
	valid_path3((X1, Y1), (X2, Y2), Valid_path, G),
	not(land_or_dropped(X2, Y2)),
	G = 1.

valid_path1((X1, Y1), (X2, Y2), [], 0) :-
	valid_path3((X1, Y1), (X2, Y2), _, G),
	land_or_dropped(X2, Y2),
	G = 1.

valid_path1((X1, Y1), (X2, Y2), [], 0) :-
	valid_path3((X1, Y1), (X2, Y2), _, G),
	G > 1.

% special case
% goal is agent current position
valid_path2((X1, Y1), (X1, Y1), [], 1, 3).

valid_path2((X1, Y1), (X2, Y2), Valid_path, Insert_goal, Len) :-
	valid_path1((X1, Y1), (X2, Y2), Valid_path, Insert_goal),
	length(Valid_path, Len).


% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% Q4
% make a plan to goal(X,Y) from current location
% and take an action
%
% 		get_action(+Intentions, -Intentions1, -Action)
% 		   -Intentions is a list of intents
% 			Intentions1 is a list of intents updated with plan 
% 			Action is an action need to take in this cycle which may be move, pick or drop 
% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %

% agent has a stone: drop 
% without a plan 
get_action(intents([[goal(X6, Y6),[]]|Tail4], Int_pick), intents([[goal(X6, Y6),Tail5]|Tail4], Int_pick), H1) :-
	agent_stones(1),
	selected_drop([[goal(X6, Y6),[]]|Tail4], [[goal(X6, Y6),[H1|Tail5]]|Tail4]).

% with an applicable plan 
get_action(intents([[goal(X6, Y6),[H1|Tail5]]|Tail4], Int_pick), intents([[goal(X6, Y6),Tail5]|Tail4], Int_pick), H1) :-
	agent_stones(1),
	applicable(H1).

% with a not applicable plan 
get_action(intents([[goal(X6, Y6),[H1|_]]|Tail4], Int_pick), intents([[goal(X7, Y7),T6]|Tail4], Int_pick), H2) :-
	agent_stones(1),
	not(applicable(H1)),
	selected_drop([[goal(X6, Y6),[]]|Tail4], [[goal(X7, Y7),[H2|T6]]|Tail4]).

% agent does not have a stone: pick 
% no pick intentions
get_action(intents(Int_drop, []), intents(Int_drop, []), move(Xagent, Yagent)) :-
	agent_stones(0),
	agent_at(Xagent, Yagent).

% without a plan 
get_action(intents(Int_drop, [[goal(X6, Y6),[]]|Tail4]), intents(Int_drop, [[goal(X6, Y6),Tail5]|Tail4]), H1) :-
	agent_stones(0),
	selected_pick([[goal(X6, Y6),[]]|Tail4], [[goal(X6, Y6),[H1|Tail5]]|Tail4]).

% with an applicable plan 
get_action(intents(Int_drop, [[goal(X6, Y6),[H1|Tail5]]|Tail4]), intents(Int_drop, [[goal(X6, Y6),Tail5]|Tail4]), H1) :-
	agent_stones(0),
	applicable(H1).

% with a not applicable plan 
get_action(intents(Int_drop, [[goal(X6, Y6),[H1|_]]|Tail4]), intents(Int_drop, [[goal(X7, Y7),T6]|T4]), H2) :-
	agent_stones(0),
	not(applicable(H1)),
	selected_pick([[goal(X6, Y6),[]]|Tail4], [[goal(X7, Y7),[H2|T6]]|T4]).

% make a pick plan 
selected_pick([[goal(X5, Y5),[]]| Tail3], Intentions1) :-
	plan_pick(goal(X5, Y5), Plan_pick),
	Intentions1 = [[goal(X5, Y5),Plan_pick] | Tail3].

% make a drop plan 
selected_drop([[goal(X5, Y5),[]]| Tail3], Intentions1) :-
	plan_drop(goal(X5, Y5), Plan_pick),
	Intentions1 = [[goal(X5, Y5), Plan_pick] | Tail3].

% pick plan 
% special case
% stones is on the agent position 
plan_pick(goal(Xpick, Ypick), [move(Xpick1, Ypick1), pick(Xpick, Ypick)]) :-
	agent_at(Xpick, Ypick),
	Xpick1 is Xpick - 1,
	Ypick1 is Ypick,
	land_or_dropped(Xpick1, Ypick1).

plan_pick(goal(Xpick, Ypick), [move(Xpick1, Ypick1), pick(Xpick, Ypick)]) :-
	agent_at(Xpick, Ypick),
	Xpick1 is Xpick + 1,
	Ypick1 is Ypick,
	land_or_dropped(Xpick1, Ypick1).

plan_pick(goal(Xpick, Ypick), [move(Xpick1, Ypick1), pick(Xpick, Ypick)]) :-
	agent_at(Xpick, Ypick),
	Xpick1 is Xpick,
	Ypick1 is Ypick - 1,
	land_or_dropped(Xpick1, Ypick1).

plan_pick(goal(Xpick, Ypick), [move(Xpick1, Ypick1), pick(Xpick, Ypick)]) :-
	agent_at(Xpick, Ypick),
	Xpick1 is Xpick,
	Ypick1 is Ypick + 1,
	land_or_dropped(Xpick1, Ypick1).

% calculate a valid path and modified it into actions
plan_pick(goal(Xpick, Ypick), Plan_pick) :-
	agent_at(Xagent, Yagent),
	valid_path((Xagent, Yagent), (Xpick, Ypick), Valid_path1, _),
	plan_pick1(Valid_path1, Plan_pick).

% generates move actions by plan_pick2()
% add last pick action 
plan_pick1([(X4, Y4)|Tail1], Plan_pick) :-
	append(Plan_pick1, [pick(X4, Y4)], Plan_pick),
	plan_pick2(Tail1, Plan_pick1).

% base case 
plan_pick2([(_, _)], []).

% recursive part
plan_pick2([(X3, Y3)|Tail2], Plan_pick2) :-
	append(Plan_pick3, [move(X3, Y3)], Plan_pick2),
	plan_pick2(Tail2, Plan_pick3).

% drop plan 
% similar to pick plan 
plan_drop(goal(Xdrop, Ydrop), Plan_drop) :-
	agent_at(Xagent, Yagent),
	valid_path((Xagent, Yagent), (Xdrop, Ydrop), Valid_path2, _),
	plan_drop1(Valid_path2, Plan_drop).

plan_drop1([(X4, Y4)|Tail1], Plan_drop) :-
	append(Plan_drop1, [drop(X4, Y4)], Plan_drop),
	plan_drop2(Tail1, Plan_drop1).

plan_drop2([(_, _)], []).

plan_drop2([(X3, Y3)|Tail2], Plan_drop2) :-
	append(Plan_drop3, [move(X3, Y3)], Plan_drop2),
	plan_drop2(Tail2, Plan_drop3).

% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %
% Q5
% based on observation, updates agent intentions
%
% 		update_intentions(+Observation, +Intentions2, -Intentions3) 
%          -Observation is a state of agent, in form of at(), picked() or dropped()
% 			Intentions2 is a list of intentions
% 		e.g.
% 		?- update_intentions(at(9,8),intents([[goal(9,9),[drop(9,9)]]],[]),Intentions3).
% 		Intentions3 = intents([[goal(9, 9), [drop(9, 9)]]], []).
% 		?- update_intentions(picked(9,6),intents([[goal(9,9),[]]],[[goal(9,6),[]]]),Intentions3).
% 		Intentions3 = intents([[goal(9, 9), []]], []).
% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % %

% at() 
update_intentions(at(_,_), Intentions, Intentions).

% dropped(), delete first element in Int_drop
update_intentions(dropped(_,_), intents([_|T],Int_pick), intents(T,Int_pick)).

% picked(), delete first element in Int_pick
update_intentions(picked(_,_), intents(Int_drop, [_|T]), intents(Int_drop, T)).

% below is copy of [pathsearch] and [ucsdijkstra]

% pathsearch.pl

% COMP3411/9414/9814 Artificial Intelligence, UNSW, Alan Blair

% This file provides code for insert_legs(), head_member() and build_path()
% used by bfsdijkstra(), ucsdijkstra(), greedy() and astar().

% insert_legs(Generated, Legs, Generated1).
% insert new legs into list of generated legs,
% by repeatedly calling insert_one_leg()

% base case: no legs to be inserted
insert_legs(Generated, [], Generated).

% Insert the first leg using insert_one_leg(); and continue.
insert_legs(Generated, [Leg|Legs], Generated2) :-
   insert_one_leg(Generated, Leg, Generated1),
   insert_legs(Generated1, Legs, Generated2).

% head_member(Node, List)
% check whether Node is the head of a member of List.

% base case: node is the head of first item in list.
head_member(Node,[[Node,_]|_]).

% otherwise, keep searching for node in the tail.
head_member(Node,[_|Tail]) :-
  head_member(Node,Tail).

% build_path(Expanded, [[Node,Pred]], Path).

% build_path(Legs, Path)
% Construct a path from a list of legs, by joining the ones that match.

% base case: join the last two legs to form a path of one step.
build_path([[Next,Start],[Start,Start]], [Next,Start]).

% If the first two legs match, add to the front of the path.
build_path([[C,B],[B,A]|Expanded],[C,B,A|Path]) :-
   build_path([[B,A]|Expanded],[B,A|Path]), ! .

% If the above rule fails, we skip the next leg in the list.
build_path([Leg,_SkipLeg|Expanded],Path) :-
   build_path([Leg|Expanded],Path).

% Uniform Cost Search, using Dijkstras Algorithm

% COMP3411/9414/9814 Artificial Intelligence, UNSW, Alan Blair

% solve(Start, Solution, G, N)
% Solution is a path (in reverse order) from start node to a goal state.
% G is the length of the path, N is the number of nodes expanded.

solve(Start, Solution, G, N)  :-
    ucsdijkstra([[Start,Start,0]], [], Solution, G, 1, N).

% ucsdijkstra(Generated, Expanded, Solution, L, N)
%
% The algorithm builds a list of generated "legs" in the form
% Generated = [[Node1,Prev1,G1],[Node2,Prev2,G2],...,[Start,Start,0]]
% The path length G from the start node is stored with each leg,
% and the legs are listed in increasing order of G.
% The expanded nodes are moved to another list (G is discarded)
%  Expanded = [[Node1,Prev1],[Node2,Prev2],...,[Start,Start]]

% If the next leg to be expanded reaches a goal node,
% stop searching, build the path and return it.
ucsdijkstra([[Node,Pred,G]|_Generated], Expanded, Path, G, N, N)  :-
    goal(Node),
    build_path([[Node,Pred]|Expanded], Path).

% Extend the leg at the head of the queue by generating the
% successors of its destination node.
% Insert these newly created legs into the list of generated nodes,
% keeping it sorted in increasing order of G; and continue searching.
ucsdijkstra([[Node,Pred,G]| Generated], Expanded, Solution, G1, L, N) :-
    extend(Node, G, Expanded, NewLegs),
    M is L + 1,
    insert_legs(Generated, NewLegs, Generated1),
    ucsdijkstra(Generated1, [[Node,Pred]|Expanded], Solution, G1, M, N).

% Find all successor nodes to this node, and check in each case
% that the new node has not previously been expanded.
extend(Node, G, Expanded, NewLegs) :-
    % write(Node),nl,   % print nodes as they are expanded
    findall([NewNode, Node, G1], (s(Node, NewNode, C)
    , not(head_member(NewNode, Expanded))
    , G1 is G + C
    ), NewLegs).

% base case: insert leg into an empty list.
insert_one_leg([], Leg, [Leg]).

% If we already knew a shorter path to the same node, discard the new one.
insert_one_leg([Leg1|Generated], Leg, [Leg1|Generated]) :-
    Leg  = [Node,_Pred, G ],
    Leg1 = [Node,_Pred1,G1],
    G >= G1, ! .

% Insert the new leg in its correct place in the list (ordered by G).
insert_one_leg([Leg1|Generated], Leg, [Leg,Leg1|Generated]) :-
    Leg  = [_Node, _Pred, G ],
    Leg1 = [_Node1,_Pred1,G1],
    G < G1, ! .

% Search recursively for the correct place to insert.
insert_one_leg([Leg1|Generated], Leg, [Leg1|Generated1]) :-
    insert_one_leg(Generated, Leg, Generated1).

% Uniform Cost Search, using Dijkstras Algorithm

solve1(Start, Solution, G, N)  :-
    ucsdijkstra1([[Start,Start,0]], [], Solution, G, 1, N).

% ucsdijkstra(Generated, Expanded, Solution, L, N)
%
% The algorithm builds a list of generated "legs" in the form
% Generated = [[Node1,Prev1,G1],[Node2,Prev2,G2],...,[Start,Start,0]]
% The path length G from the start node is stored with each leg,
% and the legs are listed in increasing order of G.
% The expanded nodes are moved to another list (G is discarded)
%  Expanded = [[Node1,Prev1],[Node2,Prev2],...,[Start,Start]]

% If the next leg to be expanded reaches a goal node,
% stop searching, build the path and return it.
ucsdijkstra1([[Node,Pred,G]|_Generated], Expanded, Path, G, N, N)  :-
    goal1(Node),
    build_path([[Node,Pred]|Expanded], Path).

% Extend the leg at the head of the queue by generating the
% successors of its destination node.
% Insert these newly created legs into the list of generated nodes,
% keeping it sorted in increasing order of G; and continue searching.
ucsdijkstra1([[Node,Pred,G]| Generated], Expanded, Solution, G1, L, N) :-
    extend1(Node, G, Expanded, NewLegs),
    M is L + 1,
    insert_legs(Generated, NewLegs, Generated1),
    ucsdijkstra1(Generated1, [[Node,Pred]|Expanded], Solution, G1, M, N).

% Find all successor nodes to this node, and check in each case
% that the new node has not previously been expanded.
extend1(Node, G, Expanded, NewLegs) :-
    % write(Node),nl,   % print nodes as they are expanded
    findall([NewNode, Node, G1], (s1(Node, NewNode, C)
    , not(head_member(NewNode, Expanded))
    , G1 is G + C
    ), NewLegs).
