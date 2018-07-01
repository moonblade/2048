from game import Game
from brain import DeepQNetwork

nEpisodes = 300
def run():
	step = 0
	for episode in range(nEpisodes):
		state = game.reset()
		while True:
			action = RL.chooseAction(state)
			observation, reward, done = game.step(action)
			RL.storeTransition(state, action, reward, observation)

			if step > 200 and step%5==0:
				RL.learn()

			state = observation

			if done:
				break
			step+=1
		print("score : ", game.score, game.board.getState())
	print('done')


if __name__ == '__main__':
	game = Game()
	RL = DeepQNetwork(game.nActions, game.nFeatures, learningRate=0.01, replaceTarget=200, memorySize=2000)
	run()
