import { Card, Title, Text } from "@tremor/react";

export default function FeatureExtraction() {
  return (
    <div className="space-y-6">
      <div>
        <Title>特征提取</Title>
        <Text>即将上线：从原始 K 线提取结构化交易特征。</Text>
      </div>
      <div className="grid gap-6 lg:grid-cols-3">
        <Card>
          <Title>价格形态</Title>
          <Text>顶底结构、趋势段、震荡区间。</Text>
        </Card>
        <Card>
          <Title>量能结构</Title>
          <Text>放量/缩量分布与分型。</Text>
        </Card>
        <Card>
          <Title>均线与波动</Title>
          <Text>多周期均线关系与波动率刻画。</Text>
        </Card>
      </div>
    </div>
  );
}
