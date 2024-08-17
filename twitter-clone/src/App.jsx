import { Heart, MessageCircle, Repeat2 } from "lucide-react";

const tweets = [
  {
    username: "johndoe",
    publicName: "John Doe",
    profilePicUrl: "/api/placeholder/50/50",
    tweet: "Just had an amazing day at the beach! 🏖️ #summervibes",
    likes: 42,
    retweets: 12,
    replies: 5,
  },
  {
    username: "janedoe",
    publicName: "Jane Doe",
    profilePicUrl: "/api/placeholder/50/50",
    tweet: "Check out my new blog post on React hooks! 🚀 #reactjs #webdev",
    likes: 89,
    retweets: 34,
    replies: 15,
  },
];

const Tweet = ({ tweet }) => (
  <div className="border-b border-gray-200 p-4">
    <div className="flex items-start">
      <img
        src={tweet.profilePicUrl}
        alt={tweet.publicName}
        className="w-12 h-12 rounded-full mr-4"
      />
      <div className="flex-1">
        <div className="flex items-center">
          <h4 className="font-bold">{tweet.publicName}</h4>
          <span className="text-gray-500 ml-2">@{tweet.username}</span>
        </div>
        <p className="mt-1">{tweet.tweet}</p>
        <div className="flex mt-2 text-gray-500">
          <button className="flex items-center mr-4">
            <MessageCircle size={18} className="mr-1" />
            <span>{tweet.replies}</span>
          </button>
          <button className="flex items-center mr-4">
            <Repeat2 size={18} className="mr-1" />
            <span>{tweet.retweets}</span>
          </button>
          <button className="flex items-center">
            <Heart size={18} className="mr-1" />
            <span>{tweet.likes}</span>
          </button>
        </div>
      </div>
    </div>
  </div>
);

const TwitterClone = () => (
  <div className="max-w-2xl mx-auto bg-white shadow-md overflow-hidden">
    <div className="bg-blue-500 text-white p-4">
      <h1 className="text-2xl font-bold">Home</h1>
    </div>
    <div>
      {tweets.map((tweet, index) => (
        <Tweet key={index} tweet={tweet} />
      ))}
    </div>
  </div>
);

export default TwitterClone;
