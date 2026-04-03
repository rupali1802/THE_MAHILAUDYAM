/**
 * Product Images Utility
 * Maps commodity names to high-quality product images from Unsplash
 */

export const PRODUCT_IMAGES = {
  'rice': 'https://images.unsplash.com/photo-1595433707802-6b2626ef1c91?w=400&h=300&fit=crop',
  'wheat': 'https://images.unsplash.com/photo-1585979949075-ade4e5c8b651?w=400&h=300&fit=crop',
  'onion': 'https://images.unsplash.com/photo-1585518419759-4b61ecc3e4b6?w=400&h=300&fit=crop',
  'carrot': 'https://images.unsplash.com/photo-1447175008436-054170c2e601?w=400&h=300&fit=crop',
  'tomato': 'https://images.unsplash.com/photo-1532694215381-6c9c90162036?w=400&h=300&fit=crop',
  'potato': 'https://images.unsplash.com/photo-1596363860416-bf4e4b30287b?w=400&h=300&fit=crop',
  'banana': 'https://images.unsplash.com/photo-1571407614161-c3ce9b55aacd?w=400&h=300&fit=crop',
  'mango': 'https://images.unsplash.com/photo-1553279768-865a24cda92f?w=400&h=300&fit=crop',
  'apple': 'https://images.unsplash.com/photo-1560806674-104fc7c55c24?w=400&h=300&fit=crop',
  'orange': 'https://images.unsplash.com/photo-1564241158518-d9c9e562d5fd?w=400&h=300&fit=crop',
  'milk': 'https://images.unsplash.com/photo-1563636619-51f2b652fcd2?w=400&h=300&fit=crop',
  'ghee': 'https://images.unsplash.com/photo-1608849823803-97d6b6b3c869?w=400&h=300&fit=crop',
  'yogurt': 'https://images.unsplash.com/photo-1599599810694-02278e42f89b?w=400&h=300&fit=crop',
  'paneer': 'https://images.unsplash.com/photo-1452821952904-5573d96a54fa?w=400&h=300&fit=crop',
  'turmeric': 'https://images.unsplash.com/photo-1599599810694-02278e42f89b?w=400&h=300&fit=crop&q=80',
  'chili': 'https://images.unsplash.com/photo-1599599810694-02278e42f89b?w=400&h=300&fit=crop',
  'chili powder': 'https://images.unsplash.com/photo-1599599810694-02278e42f89b?w=400&h=300&fit=crop',
  'coconut': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=300&fit=crop',
  'coriander': 'https://images.unsplash.com/photo-1599599810694-02278e42f89b?w=400&h=300&fit=crop',
  'coriander powder': 'https://images.unsplash.com/photo-1599599810694-02278e42f89b?w=400&h=300&fit=crop',
  'black pepper': 'https://images.unsplash.com/photo-1599599810694-02278e42f89b?w=400&h=300&fit=crop',
  'coconut oil': 'https://images.unsplash.com/photo-1599599810694-02278e42f89b?w=400&h=300&fit=crop',
  'sesame oil': 'https://images.unsplash.com/photo-1599599810694-02278e42f89b?w=400&h=300&fit=crop',
  'pickle': 'https://images.unsplash.com/photo-1599599810694-02278e42f89b?w=400&h=300&fit=crop',
  'pickle (mango)': 'https://images.unsplash.com/photo-1599599810694-02278e42f89b?w=400&h=300&fit=crop',
  'jams': 'https://images.unsplash.com/photo-1589985643862-b53b6f85b0bb?w=400&h=300&fit=crop',
  'dry snacks': 'https://images.unsplash.com/photo-1585667228485-d0a7f7a3caa8?w=400&h=300&fit=crop',
  'handmade cloth': 'https://images.unsplash.com/photo-1540553016-e8290a976fcb?w=400&h=300&fit=crop',
  'embroidered saree': 'https://images.unsplash.com/photo-1590080876-0cd4e0b7b858?w=400&h=300&fit=crop',
  'handmade jewelry': 'https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=400&h=300&fit=crop',
  'wooden craft': 'https://images.unsplash.com/photo-1578500494198-246f612d03b3?w=400&h=300&fit=crop'
};

/**
 * Get product image URL by commodity name
 * Supports exact and fuzzy matching
 */
export function getProductImage(commodityName) {
  if (!commodityName) return null;
  
  const key = commodityName.toLowerCase().trim();
  
  // Direct match first
  if (PRODUCT_IMAGES[key]) {
    return PRODUCT_IMAGES[key];
  }
  
  // Try fuzzy matching for variations
  for (const [mappedKey, imageUrl] of Object.entries(PRODUCT_IMAGES)) {
    if (key.includes(mappedKey) || mappedKey.includes(key)) {
      return imageUrl;
    }
  }
  
  return null;
}

/**
 * Enrich items with product images
 * @param {Array} items - Market price items
 * @returns {Array} Items with image property added
 */
export function enrichItemsWithImages(items) {
  if (!Array.isArray(items)) {
    console.warn('enrichItemsWithImages: items is not an array');
    return items;
  }
  
  const enriched = items.map(item => {
    const imageUrl = getProductImage(item.commodity_name);
    return {
      ...item,
      image: imageUrl || null
    };
  });
  
  console.log(`✅ Enriched ${enriched.length} items with images`);
  enriched.slice(0, 3).forEach(item => {
    console.log(`  📦 ${item.commodity_name}: ${item.image ? '✓ Has image' : '✗ No image'}`);
  });
  
  return enriched;
}
