// src/components/Head/keywords.ts
export const defaultKeywordsRaw = `
Japan
Bike Tour
Biking Japan
Bike Japan
Rural Japan Tour
Bikepacking Trip Japan
Japan Bike Tour
Japan Cycling Tour
Japan Cycling
Japan Cycling Trips
Japan Cycling Tours
Japan Cycling Holidays
Japan Cycling Adventures
Family Friendly Japan Tour
Family Friendly Japan Countryside Tour
Family Friendly Japan Rural Tour
Family Travel Ideas Japan
Family Travel JapanJapan
Family Bike Trips Japan
Family Activities Japan
Hike Tour
Rural Japan
Countryside Japan
Custom Japan Tour
Guided Tours Japan
self Guided Japan Tour
Self Guided Walking Tours Japan
Hiking Japan
Japan Outdoor Tours
Bike Trips Japan
Walking Tours Japan
Nature Tours Japan
Japan Adventure Travel
Japanese Countryside
Rural Japan Tours
Japan Travel
Japan Eco Tours
Hiking Japan
Cycling Tours Japan
Outdoor Activities Japan
Active Travel Japan
`;

export const defaultKeywordsArray = defaultKeywordsRaw
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter((line) => line.length > 0);

export const defaultKeywordsList = defaultKeywordsArray.join(', ');
