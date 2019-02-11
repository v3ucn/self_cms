
##主要功能
好近的社交部分, 功能包含顶帖、消息中心, 作为一个submodule, 内嵌于honey_manage, near-api, weidian_app等项目

###redis的key命名
	 
	 #### 用户, sortedset
	 * 用户顶的帖子列表
	     * key: user_{user_id}_up_posts
	     * member: posts_id `<int>`
	     * score: timestamp `<int>`   eg: 14923548
	     
	 #### 帖子, sortedset
	 * 顶该帖子的用户列表
	     * key: near_posts_{post_id}_up
	     * member: user_id `<int>`
	     * score: timestamp `<int>`   eg: 14923548

     * 顶该帖子的用户历史列表，取消顶不删，以后会加过期时间
         * key: near_posts_{post_id}_up_history
	     * member: user_id `<int>`
	     * score: timestamp `<int>`   eg: 14923548

	 #### 消息中心, sortedset
	     * key: msg_{user_id}_me
	     * member: {msg_id}  `<str>` eg: 5d1d7710d0474579ae99029fb2681773
	     * score: timestamp `<int>`   eg: 14923548
	     
	 #### 消息内容, hash
	     * key: msg_{user_id}_detail
	     * field: {msg_id}  `<str>` eg: 5d1d7710d0474579ae99029fb2681773
	     * value: 二进制消息体，通过protobuf反序列化，可得到.格式如下


###消息体的protobuf格式定义：

		message User
        {
            required int32 user_id = 1;      // 用户ID
            required string nickname = 2;    // 昵称
            required string avatar = 3;      // 头像
        }
        message Msg
        {
            required string msg_id = 1;      // 消息ID
            required Msgtype type = 2;       // 消息类型
            required string content = 3;     // 消息内容
            required string topic_id = 4;    // 话题ID
            required string topic_name = 5;  // 话题名称
            optional string post_id = 6;     // 帖子ID
            optional string post_img = 7;    // 帖子图片
            optional string timestamp = 8;   // 时间戳
            optional int32 actiontype = 9;   // 是否跳转
            optional string url = 10;        // 跳转url地址
            repeated User users = 11;        // 用户列表
            enum Msgtype
            {
                SYSTEM = 0;                 // 系统
                AUDIT_PASS = 21;            // 审核通过
                AUDIT_NOPASS = 22;          // 审核失败
                POST_UP = 23;               // 顶贴
                POST_REPLY = 24;            // 回帖
                GOOD_BEGIN = 25;            // 特卖开始
                COMMENT_REPLY = 26;         // 评论
            }
        }