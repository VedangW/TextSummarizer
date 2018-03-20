from gensim.models import Word2Vec
# define training data
# sentences = [['this', 'is', 'the', 'first', 'sentence', 'for', 'word2vec'],
# 			['this', 'is', 'the', 'second', 'sentence'],
# 			['yet', 'another', 'sentence'],
# 			['one', 'more', 'sentence'],
# 			['and', 'the', 'final', 'sentence']]

sentences1 = [['leave', 'my', 'class'],
			['I', 'hate', 'tirtharaj'],
			['World', 'war', 'tirtharaj', 'die'],
			['house', 'on', 'the', 'hate', 'hill']]

sentences2 = [['I', 'hate', 'tirtharaj'],
			['World', 'war', 'tirtharaj', 'die'],
			['house', 'on', 'the', 'hate', 'hill']]

# train model
model = Word2Vec(sentences1, min_count=1)
# summarize the loaded model
print(model)
# summarize vocabulary
words = list(model.wv.vocab)
print(words)
# access vector for one word
x1 = model['tirtharaj']
# save model
# model.save('model.bin')
# load model
# new_model = Word2Vec.load('model.bin')
# print(new_model)

model1 = Word2Vec(sentences2, min_count=1)
# summarize the loaded model
print(model)
# summarize vocabulary
words = list(model1.wv.vocab)
print(words)
# access vector for one word
x2 = model1['tirtharaj']
# save model
# model.save('model.bin')
# load model
# new_model = Word2Vec.load('model.bin')
# print(new_model)

print x1.all() == x2.all()
