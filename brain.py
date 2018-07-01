import numpy as np
import tensorflow as tf
from move import Move

np.random.seed(1)
tf.set_random_seed(1)

class DeepQNetwork():
	def __init__(self, nActions, nFeatures, learningRate=0.1, rewardDecay=0.9, epsilonGreedy=0.9, replaceTarget=300, memorySize=500, batchSize=32, epsilonGreedyInc=.01):
		self.nActions = nActions;
		self.nFeatures = nFeatures;
		self.learningRate = learningRate;
		self.rewardDecay = rewardDecay;
		self.epsilonGreedy = epsilonGreedy;
		self.replaceTarget = replaceTarget;
		self.memorySize = memorySize;
		self.batchSize = batchSize;
		self.epsilonGreedyInc = epsilonGreedyInc;
		self.epsilon = epsilonGreedy;
		# self.epsilon = 0;

		self.stepCounter = 0;

		# [s,a,s_,r]
		self.memory = np.zeros((self.memorySize, self.nFeatures*2 + 2))
		self.memoryCounter = 0

		self.buildNet()

		tParams = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope='target');
		eParams = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope='eval');

		with tf.variable_scope('softReplace'):
			self.targetReplace = [tf.assign(t, e) for t,e in zip(tParams, eParams)]

		self.session = tf.Session()
		self.session.run(tf.global_variables_initializer())

	def buildNet(self):
		self.state = tf.placeholder(tf.float32, [None, self.nFeatures], name='state')
		self.observation = tf.placeholder(tf.float32, [None, self.nFeatures], name='observation')
		self.reward = tf.placeholder(tf.float32, [None, ], name='reward')
		self.action = tf.placeholder(tf.int32, [None, ], name='action')

		wInitializer, bInitializer = tf.random_normal_initializer(0., 0.3), tf.constant_initializer(0.1)

		# eval
		with tf.variable_scope('eval'):
			e1 = tf.layers.dense(self.state, 20, tf.nn.relu, kernel_initializer= wInitializer, bias_initializer= bInitializer, name='e1')
			self.qEval = tf.layers.dense(e1, self.nActions, kernel_initializer= wInitializer, bias_initializer=bInitializer, name='qEval')

		with tf.variable_scope('target'):
			t1 = tf.layers.dense(self.observation, 20, tf.nn.relu, kernel_initializer=wInitializer, bias_initializer=bInitializer, name='t1')
			self.qNext = tf.layers.dense(t1, self.nActions, kernel_initializer=wInitializer, bias_initializer=bInitializer, name='qNext')

		with tf.variable_scope('qTarget'):
			qTarget = self.reward + self.rewardDecay * tf.reduce_max(self.qNext, axis=1, name='qMaxObserveration')
			self.qTarget = tf.stop_gradient(qTarget)

		with tf.variable_scope('qEval'):
			actionIndices = tf.stack([tf.range(tf.shape(self.action)[0], dtype=tf.int32), self.action], axis=1)
			self.qEvalWrtAction = tf.gather_nd(params=self.qEval, indices=actionIndices)

		with tf.variable_scope('loss'):
			self.loss = tf.reduce_mean(tf.squared_difference(self.qTarget, self.qEvalWrtAction, name='loss'))

		with tf.variable_scope('train'):
			self.trainOp = tf.train.RMSPropOptimizer(self.learningRate).minimize(self.loss)

	def chooseAction(self, observation):
		observation = observation[np.newaxis, :]

		if np.random.uniform() < self.epsilon:
			actionsValue = self.session.run(self.qEval, feed_dict={self.state: observation})
			action = np.argmax(actionsValue)
		else:
			action = np.random.randint(0, self.nActions)
		return action

	def storeTransition(self, state, action, reward, observation):
		transition = np.hstack((state, [action, reward], observation))
		index = self.memoryCounter % self.memorySize
		self.memory[index, :] = transition
		self.memoryCounter+=1

	def learn(self):
		if self.stepCounter % self.replaceTarget == 0:
			self.session.run(self.targetReplace)

		if self.memoryCounter > self.memorySize:
			sampleIndex = np.random.choice(self.memorySize, size=self.batchSize)
		else:
			sampleIndex = np.random.choice(self.memoryCounter, size= self.batchSize)

		batchMemory = self.memory[sampleIndex, :]

		_, cost = self.session.run([self.trainOp, self.loss], feed_dict={
			self.state: batchMemory[:, :self.nFeatures],
			self.action: batchMemory[:, self.nFeatures],
			self.reward: batchMemory[:, self.nFeatures+1],
			self.observation: batchMemory[:, -self.nFeatures:]
		})

		self.epsilon = self.epsilon + self.epsilonGreedyInc if self.epsilon < self.epsilonGreedy else self.epsilonGreedy


if __name__ == '__main__':
	DeepQNetwork(4, 16)