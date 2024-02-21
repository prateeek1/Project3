
import findspark
findspark.init()
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

spark = SparkSession.builder.appName("YourAppName").getOrCreate()
df=spark.read.csv("dataset.csv",header=True)
unique_list = []
for i in range(1, 4920):
    row = df.collect()[i]
    
    for j in range(1, len(row)):
        if row[j] is None:
            break
        
        value = str(row[j]).replace('_', ' ')
        if value not in unique_list:
            unique_list.append(value)

print(unique_list)


from pyspark.sql.functions import col, when
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

disease = []
symptom = []
print(len(unique_list))
for i in range(1,4920):

    row = df.collect()[i]
    col = [0] * len(unique_list)
    d=[]
    d.append(row[0])
    symptom = []
    
    for j in range(1, len(row)):
        if row[j] is None:
            break
        
        symptom.append(row[j].replace('_',' '))
    
    
    for j in range(len(unique_list)):
        if unique_list[j] in symptom:
            d.append(1)
        else:
            d.append(0)
    disease.append(d)


schema = StructType([StructField("disease", StringType(), True)] + [StructField(symptom, IntegerType(), True) for symptom in unique_list])
df_upd = spark.createDataFrame([(disease[i]) for i in range(len(disease))], schema=schema)

df_upd.printSchema()

from pyspark.ml.feature import VectorAssembler
assembler = VectorAssembler(inputCols=unique_list, outputCol="features")
df_upd = assembler.transform(df_upd)

df_upd.show(2)


from pyspark.ml.feature import StringIndexer

label_stringIdx = StringIndexer(inputCol = 'disease', outputCol = 'labelIndex')
df_upd1 = label_stringIdx.fit(df_upd).transform(df_upd)

train, test = df_upd1.randomSplit([0.8, 0.2], seed = 2018)
print("Training Dataset Count: " + str(train.count()))
print("Test Dataset Count: " + str(test.count()))

from pyspark.ml.classification import RandomForestClassifier

rf = RandomForestClassifier(featuresCol = 'features', labelCol = 'labelIndex')
rfModel = rf.fit(train)
predictions = rfModel.transform(test)

from pyspark.ml.evaluation import MulticlassClassificationEvaluator

evaluator = MulticlassClassificationEvaluator(labelCol="labelIndex", predictionCol="prediction")
accuracy = evaluator.evaluate(predictions)
print("Accuracy = %s" % (accuracy))
print("Test Error = %s" % (1.0 - accuracy))

from pyspark.mllib.evaluation import MulticlassMetrics
from pyspark.sql.types import FloatType
import pyspark.sql.functions as F

preds_and_labels = predictions.select(['prediction','labelIndex']).withColumn('labelIndex', F.col('labelIndex').cast(FloatType())).orderBy('prediction')
preds_and_labels = preds_and_labels.select(['prediction','labelIndex'])
metrics = MulticlassMetrics(preds_and_labels.rdd.map(tuple))
print(metrics.confusionMatrix().toArray())







from pyspark.ml.classification import DecisionTreeClassifier
rf = DecisionTreeClassifier(featuresCol = 'features', labelCol = 'labelIndex')
rfModel = rf.fit(train)
predictions = rfModel.transform(test)


