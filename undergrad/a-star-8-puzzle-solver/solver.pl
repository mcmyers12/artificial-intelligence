%top right corner
move([0,A,B, C,D,E, F,G,H],[A,0,B, C,D,E, F,G,H]).
move([0,A,B, C,D,E, F,G,H],[C,A,B, 0,D,E, F,G,H]).

%top left corner
move([A,B,0, C,D,E, F,G,H],[A,0,B, C,D,E, F,G,H]).
move([A,B,0, C,D,E, F,G,H],[C,A,B, 0,D,E, F,G,H]).

%bottom right corner
move([A,B,C, D,E,F, G,H,0],[A,B,C, D,E,F, G,0,H]).
move([A,B,C, D,E,F, G,H,0],[A,B,C, D,E,0, G,H,F]).

%bottom left corner
move([A,B,C, D,E,F, 0,G,H],[A,B,C, D,E,F, G,0,H]).
move([A,B,C, D,E,F, 0,G,H],[A,B,C, 0,E,F, D,G,H]).

%top middle
move([A,0,B, C,D,E, F,G,H],[A,D,B, C,0,E, F,G,H]).
move([A,0,B, C,D,E, F,G,H],[0,A,B, C,D,E, F,G,H]).
move([A,0,B, C,D,E, F,G,H],[A,B,0, C,D,E, F,G,H]).

%left middle
move([A,B,C, 0,D,E, F,G,H],[A,B,C, D,0,E, F,G,H]).
move([A,B,C, 0,D,E, F,G,H],[0,B,C, A,D,E, F,G,H]).
move([A,B,C, 0,D,E, F,G,H],[A,B,C, F,D,E, 0,G,H]).

%right middle
move([A,B,C, D,E,0, F,G,H],[A,B,C, D,E,H, F,G,0]).
move([A,B,C, D,E,0, F,G,H],[A,B,C, D,0,E, F,G,H]).
move([A,B,C, D,E,0, F,G,H],[A,B,0, D,E,C, F,G,H]).

%bottom middle
move([A,B,C, D,E,F, G,0,H],[A,B,C, D,E,F, 0,G,H]).
move([A,B,C, D,E,F, G,0,H],[A,B,C, D,E,F, G,H,0]).
move([A,B,C, D,E,F, G,0,H],[A,B,C, D,0,F, G,E,H]).

%center middle
move([A,B,C, D,0,E, F,G,H],[A,0,C, D,B,E, F,G,H]).
move([A,B,C, D,0,E, F,G,H],[A,B,C, D,G,E, F,0,H]).
move([A,B,C, D,0,E, F,G,H],[A,B,C, 0,D,E, F,G,H]).
move([A,B,C, D,0,E, F,G,H],[A,B,C, D,E,0, F,G,H]).

loc_cost([1,A,B, C,D,E, F,G,H],0).
loc_cost([A,1,B, C,D,E, F,G,H],1).
loc_cost([A,B,1, C,D,E, F,G,H],2).
loc_cost([A,B,C, 1,D,E, F,G,H],1).
loc_cost([A,B,C, D,1,E, F,G,H],2).
loc_cost([A,B,C, D,E,1, F,G,H],3).
loc_cost([A,B,C, D,E,F, 1,G,H],2).
loc_cost([A,B,C, D,E,F, G,1,H],3).
loc_cost([A,B,C, D,E,F, G,H,1],4).


loc_cost([A,2,B, C,D,E, F,G,H],0).
loc_cost([2,A,B, C,D,E, F,G,H],1).
loc_cost([A,B,2, C,D,E, F,G,H],1).
loc_cost([A,B,C, 2,D,E, F,G,H],2).
loc_cost([A,B,C, D,2,E, F,G,H],1).
loc_cost([A,B,C, D,E,2, F,G,H],2).
loc_cost([A,B,C, D,E,F, 2,G,H],3).
loc_cost([A,B,C, D,E,F, G,2,H],2).
loc_cost([A,B,C, D,E,F, G,H,2],3).


loc_cost([A,B,3, C,D,E, F,G,H],0).
loc_cost([3,A,B, C,D,E, F,G,H],2).
loc_cost([A,3,B, C,D,E, F,G,H],1).
loc_cost([A,B,C, 3,D,E, F,G,H],3).
loc_cost([A,B,C, D,3,E, F,G,H],2).
loc_cost([A,B,C, D,E,3, F,G,H],1).
loc_cost([A,B,C, D,E,F, 3,G,H],4).
loc_cost([A,B,C, D,E,F, G,3,H],3).
loc_cost([A,B,C, D,E,F, G,H,3],2).


loc_cost([A,B,C, 4,D,E, F,G,H],0).
loc_cost([4,A,B, C,D,E, F,G,H],1).
loc_cost([A,4,B, C,D,E, F,G,H],2).
loc_cost([A,B,4, C,D,E, F,G,H],3).
loc_cost([A,B,C, D,4,E, F,G,H],1).
loc_cost([A,B,C, D,E,4, F,G,H],2).
loc_cost([A,B,C, D,E,F, 4,G,H],1).
loc_cost([A,B,C, D,E,F, G,4,H],2).
loc_cost([A,B,C, D,E,F, G,H,4],3).


loc_cost([A,B,C, D,5,E, F,G,H],0).
loc_cost([5,A,B, C,D,E, F,G,H],2).
loc_cost([A,5,B, C,D,E, F,G,H],1).
loc_cost([A,B,5, C,D,E, F,G,H],2).
loc_cost([A,B,C, 5,D,E, F,G,H],1).
loc_cost([A,B,C, D,E,5, F,G,H],1).
loc_cost([A,B,C, D,E,F, 5,G,H],2).
loc_cost([A,B,C, D,E,F, G,5,H],1).
loc_cost([A,B,C, D,E,F, G,H,5],2).



loc_cost([A,B,C, D,E,6, F,G,H],0).
loc_cost([6,A,B, C,D,E, F,G,H],3).
loc_cost([A,6,B, C,D,E, F,G,H],2).
loc_cost([A,B,6, C,D,E, F,G,H],1).
loc_cost([A,B,C, 6,D,E, F,G,H],2).
loc_cost([A,B,C, D,6,E, F,G,H],1).
loc_cost([A,B,C, D,E,F, 6,G,H],3).
loc_cost([A,B,C, D,E,F, G,6,H],2).
loc_cost([A,B,C, D,E,F, G,H,6],1).


loc_cost([A,B,C, D,E,F, 7,G,H],0).
loc_cost([7,A,B, C,D,E, F,G,H],2).
loc_cost([A,7,B, C,D,E, F,G,H],3).
loc_cost([A,B,7, C,D,E, F,G,H],4).
loc_cost([A,B,C, 7,D,E, F,G,H],1).
loc_cost([A,B,C, D,7,E, F,G,H],2).
loc_cost([A,B,C, D,E,7, F,G,H],3).
loc_cost([A,B,C, D,E,F, G,7,H],1).
loc_cost([A,B,C, D,E,F, G,H,7],2).


loc_cost([A,B,C, D,E,F, G,8,H],0).
loc_cost([8,A,B, C,D,E, F,G,H],3).
loc_cost([A,8,B, C,D,E, F,G,H],2).
loc_cost([A,B,8, C,D,E, F,G,H],3).
loc_cost([A,B,C, 8,D,E, F,G,H],2).
loc_cost([A,B,C, D,8,E, F,G,H],1).
loc_cost([A,B,C, D,E,8, F,G,H],2).
loc_cost([A,B,C, D,E,F, 8,G,H],1).
loc_cost([A,B,C, D,E,F, G,H,8],1).

loc_cost([A,B,C, D,E,F, G,H,0],0).



astartracker([1,2,3,4,5,6,7,0,8],_,_,_,[1,2,3,4,5,6,7,8,0]).
astartracker([1,2,3,4,5,6,7,0,8],_,_,_,[1,2,3,4,5,6,7,8,0]).

astartracker(OldPath,G,H,F,NewPath) :- loc_cost(OldPath,H),
	G1 is G+1,
	F is H+G1,
	move(OldPath,NewPath),
	astartracker(OldPath,G1,H,F,NewPath).

astar([1,2,3,4,5,6,7,8,0],_,_).
astar(OldPath,X,NewPath) :- astartracker(OldPath,X,0,0,NewPath).
% should I do anything for 0????

%find_loc_cost([1,A,B, C,D,E, F,G,H],X) :- X1 is X+1, find_loc_cost([1,A,B, C,D,E, F,G,H],X1).


% astar(OldPath, NewPath) :- eval(OldPath,Que), move(OldPath,NewPath).

dfs(S, Path, Path) :- goal(S).

dfs(S, Checked, Path) :-
    % try a move
    move(S, S2),
    % ensure the resulting state is new
    \+member(S2, Checked),
    % and that this state leads to the goal
    dfs(S2, [S2|Checked], Path).
